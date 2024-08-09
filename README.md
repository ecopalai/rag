# EcoPal RAG Stack
Our RAG stack consits of the following docker containers: ollama, cassandra, langflow service(langflow+postgres database)
## Docker Desktop Setup

 1. Install docker desktop: https://docs.docker.com/desktop/install/windows-install/
 1. Create bridge network net1. All of our containers will be attached to this network. Open windows powershell and run the following command:  `docker network create -d bridge net1`

## ollama Setup
1. Make sure docker desktop is running.
1. Open powershell and cd to ollama folder of this project.
1. There should be a run.bat file. Excute that file: `./run.bat`
1. Now you should see ollama container running. From browser go to http://localhost:11434 You should `Ollama is running message`
1. Installing llama3:8b model: From the docker desktop click the three dots in the Ollama container and select open in terminal
1. In the containers's terminal run this command: `ollama run llama3:8b`. Once complete it should take to the model prompt. You can exit out it.
## cassandra
This cassandra instance is required by langflow to store vecotor information.
1. From power shell cd to cassandra folder of this project.
1. `./run.bat`
1. Now you should see the cassandra container running.
1. Open cassnadra containter terminal and run `cqlsh`, you should see the prompt. Cassandra setup is done.
## Install langflow service
langflow service consists of langflow itself and postgress database.
1. From powershell cd to lanflow folder.
1. Run the command `docker compose up -d`
1. Once it is complete from browser goto http://localhost:7860 You should see the langflow user interface
## Install: Vecotor Store RAG flow
1. from the langflow UI my collection screen, click new project, button and blank project.
1. Import from `Vectore Store RAG.json`
1. There will be two flows. Top flow is to ask questions. Bottom flow takes the markdown files in the ragdata and store it in the cassandra vector store.
1. In the bottom flow press the play button in the cassandra block. This will vectorize the md files in the ragdata folder.
1. Now click the playground botton. Ask a question. 
1. Congratulations! EcoPal rag system is setup locally.
 