<template>
<div class="flex justify-center md:py-12">
  <div class="container p-3">
    <h1 class="text-2xl text-white mb-3">
      Übersicht der eingereichten Daten.
    </h1>
    <div id="map"></div>
    <ul class="list text-white">
      <li v-for="(item, index) in stats" :key="index">
        {{ item.label }} - <strong>Symptome:</strong> {{ formatSymptoms(item.symptoms) }}
      </li>
    </ul>
  </div>
</div>
</template>

<script>
  import { OpenStreetMapProvider } from 'leaflet-geosearch';
  import { groupBy } from '../utils';
export default {
  data() {
    return {
      // results: [],
      heatMapConfig: {
        // radius should be small ONLY if scaleRadius is true (or small radius is intended)
        // if scaleRadius is false it will be the constant radius used in pixels
        "radius": 20,
        "maxOpacity": .8,
        // scales the radius based on map zoom
        "scaleRadius": false,
        // if set to false the heatmap uses the global maximum for colorization
        // if activated: uses the data maximum within the current map boundaries
        //   (there will always be a red spot with useLocalExtremas true)
        "useLocalExtrema": true,
        // which field name in your data represents the latitude - default "lat"
        latField: 'lat',
        // which field name in your data represents the longitude - default "lng"
        lngField: 'lng',
        // which field name in your data represents the data value - default "value"
        valueField: 'count'
      },
      heatMapStructure: {
        max: 2,
        data: []
      },
      stats: [],
      apiResponse: [
        {
          zip_code: 12435,
          users_count_affected: 1,
          symptom: "Husten",
        },
        {
          zip_code: 12435,
          users_count_affected: 2,
          symptom: "Schnupfen",
        },
        {
          zip_code: 13355,
          users_count_affected: 10,
          symptom: "Husten",
        },
        {
          zip_code: 13355,
          users_count_affected: 211,
          symptom: "Schnupfen",
        },
      ]
    }
  },
  head() {
    return {
      title: 'tbd.',
      meta: [{
        hid: 'description',
        name: 'description',
        content: 'tbd.'
      }]
    }
  },
  async created() {
    try {
      const result = await this.$axios.$get(`${process.env.API_URL}/report/result/`);
      this.createMap(result);
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
    normalizeResponse(response) {
      const groupedResponse = groupBy(response, 'zip_code')

      return  Object.keys(groupedResponse)
        .map(zip => {
          return {
            zip: Number(zip),
            symptoms: groupedResponse[zip].map((item) => {
              return { [item.symptom]: item.users_count_affected }
            }).reduce((a, b) => Object.assign(a, b), {})
          }
        });
    },
    formatSymptoms(symptoms) {
      return Object.keys(symptoms).map((symptom, index) => {
        return `${symptom}: ${Object.values(symptoms)[index]}`;
      }).join(', ');
    },
    async createMap(response) {
      // eslint-disable-next-line no-undef
      if (document.getElementById('map')) {
        const L = this.$L;
        const HeatmapOverlay = await require('@/assets/leaflet-heatmap.js');

        const heatMapLayer = new HeatmapOverlay(this.heatMapConfig);
        const provider = new OpenStreetMapProvider();
        const results = await provider.search({ query: 'germany' });

        await this.normalizeResponse(response).forEach(async (item) => {
          try {
            const result = await provider.search({query: item.zip});
            this.stats.push({
              label: result[0].label,
              symptoms: item.symptoms
            });

            this.heatMapStructure.data.push({
              lat: Number(result[0].y),
              lng: Number(result[0].x)
            });
            heatMapLayer.setData(this.heatMapStructure)
          } catch (e) {
            console.log(e);
          }
        });

        const map = new L.Map('map', {
          dragging: !L.Browser.mobile,
          maxZoom: 10,
          tap: !L.Browser.mobile,
          center: new L.LatLng(Number(results[0].y), Number(results[0].x)),
          zoom: 6,
          layers: [new L.TileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.png'), heatMapLayer]
        });
      }
    }
  }
}
</script>

<style class="scss">
  #map {
    position: relative;
    display: block;
    height: 600px;
  }

  .list {
    padding: 20px 0;
  }
</style>
