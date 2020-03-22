covi-webapp
-----------

## Frontend - Development

See `./app` folder

## Backend - Deployment

    cd backend/deployment/ansible;
    
### Initial Deployment

     ansible-playbook common_server_setup.yml --ask-vault-pass
     ansible-playbook reverse_proxy.yml --ask-vault-pass
     ansible-playbook appdb.yml --ask-vault-pass
     ansible-playbook appdb.yml --ask-vault-pass
     ansible-playbook app.yml --ask-vault-pass
     ansible-playbook frontend.yml --ask-vault-pass
     
### Deploy Backend changes

    ansible-playbook app.yml--ask-vault-pass
    
### Deploy Frontend changes

    ansible-playbook frontend.yml--ask-vault-pass
