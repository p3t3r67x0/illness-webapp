import csv
import io
import os
import string

from django.core.management import BaseCommand, CommandError
from django.db import transaction

from ...models import Pokemon

CSV_COLUMNS_TO_CLASS_ATTR = {
    "#": "national_pokedex_number",
    "Name": "name",
    "Type 1": "type_1",
    "Type 2": "type_2",
    "Total": "total",
    "HP": "hp",
    "Attack": "attack",
    "Defense": "defense",
    "Sp. Atk": "sp_attack",
    "Sp. Def": "sp_defense",
    "Speed": "speed",
    "Generation": "generation",
}

NAME_LETTERS_DEFENSE_UP = [letter for letter in string.ascii_letters if letter != "G"]


class Command(BaseCommand):
    help = "e.g. ./manage.py datastore__import_csv --dryrun var/data/pokemon.csv"

    def add_arguments(self, parser):
        parser.add_argument("csv_file")
        parser.add_argument(
            "--dryrun", "-d", action="store_true", default=False, dest="dryrun"
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        dryrun = options["dryrun"]

        # we need a file to read
        if not os.path.exists(options["csv_file"]):
            raise CommandError(f'CSV file {options["csv_file"]} does not exist')

        # in case of reimport etc., we want to have a fresh table
        if not dryrun:
            Pokemon.objects.all().delete()

        with io.open(options["csv_file"]) as csv_fh:
            csv_reader = csv.DictReader(csv_fh)
            pokemons_imported_num = 0

            # loop over csv file rows
            for csv_row in csv_reader:
                # exclude legendary pokémon
                if csv_row["Legendary"] == "True":
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipped Legendary pokemon={csv_row['Name']}"
                        )
                    )
                    continue
                elif csv_row["Legendary"] == "False":
                    pass
                else:
                    raise NotImplementedError(
                        f"Invalid value={csv_row['Legendary']} in CSV column Legendary found. Expected True or False"
                    )

                # exclude Pokémon of type ghost
                if csv_row["Type 1"] == "Ghost" or csv_row["Type 2"] == "Ghost":
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipped pokemon={csv_row['Name']} because of type=Ghost"
                        )
                    )
                    continue

                pokemon = Pokemon()

                # map csv column to class attr and set value if not empty
                for csv_column, class_attr in CSV_COLUMNS_TO_CLASS_ATTR.items():
                    value = csv_row[csv_column]
                    if value:
                        setattr(pokemon, class_attr, value)

                # for pokémon of type Steel, double their HP
                if pokemon.type_1 == "Steel" or pokemon.type_2 == "Steel":
                    pokemon.total = int(pokemon.total) + int(pokemon.hp)
                    pokemon.hp = int(pokemon.hp) * 2
                    self.stdout.write(
                        self.style.WARNING(
                            f"Double hp of pokemon={csv_row['Name']} because of type=Steel"
                        )
                    )

                # for pokémon of type: fire, lower their attack by 10%
                if pokemon.type_1 == "Fire" or pokemon.type_2 == "Fire":
                    attack_dec = int(round(int(pokemon.attack) * 0.1))
                    pokemon.attack = int(pokemon.attack) - attack_dec
                    pokemon.total = int(pokemon.total) - attack_dec
                    self.stdout.write(
                        self.style.WARNING(
                            f"Decrease attack of pokemon={csv_row['Name']} because of type=Fire"
                        )
                    )

                # for pokémon of type bug & flying, increase their attack speed by 10%
                if (pokemon.type_1 == "Bug" and pokemon.type_2 == "Flying") or (
                    pokemon.type_1 == "Flying" and pokemon.type_2 == "Bug"
                ):
                    speed_inc = int(round(int(pokemon.speed) * 0.1))
                    pokemon.speed = int(pokemon.speed) + speed_inc
                    pokemon.total = int(pokemon.total) + speed_inc
                    self.stdout.write(
                        self.style.WARNING(
                            f"Increase attack speed of pokemon={csv_row['Name']} because of type=Bug & Flying"
                        )
                    )

                # for pokémon that start with the letter **G**, add +5 defense for every letter in their name (excluding **G**)
                if pokemon.name.startswith("G"):
                    for character in pokemon.name:
                        if character in NAME_LETTERS_DEFENSE_UP:
                            pokemon.defense = int(pokemon.defense) + 5
                            pokemon.total = int(pokemon.total) + 5
                    self.stdout.write(
                        self.style.WARNING(
                            f"Increase defense of pokemon={csv_row['Name']} because of name startswith 'G'"
                        )
                    )

                pokemons_imported_num += 1
                if not dryrun:
                    pokemon.save()

                # check totals after model has been saved and numeric values were casted to int
                pokemon.refresh_from_db()
                skills_sum = sum(
                    [
                        pokemon.defense,
                        pokemon.attack,
                        pokemon.hp,
                        pokemon.speed,
                        pokemon.sp_attack,
                        pokemon.sp_defense,
                    ]
                )
                if skills_sum != pokemon.total:
                    raise CommandError(
                        f"skills_sum({skills_sum}) != pokemon.total({pokemon.total}) for pokemon={pokemon.name} - DB Transaction rollback..."
                    )

            if not dryrun:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully imported {pokemons_imported_num} pokemons"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully completed dry run. No data was written to the database. {pokemons_imported_num} pokemons would have been written"
                    )
                )
