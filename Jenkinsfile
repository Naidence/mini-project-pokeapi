pipeline {
    agent any
    environment {
        PROJECT_ID = 'zabbix-417112'
                CLUSTER_NAME = 'k8s-project'
                LOCATION = 'us-central1-c'
                CREDENTIALS_ID = 'kubernetes'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github', url: 'https://github.com/Naidence/mini-project-pokeapi.git']])
            }
        }
        stage('Build image') {
            steps {
                script {
                    app = docker.build("razannadhif/minpropokeapi:${env.BUILD_ID}")
                    }
            }
        }

        stage('Push image') {
            steps {
                script {
                    withCredentials( \
                                 [string(credentialsId: 'dockerhub',\
                                 variable: 'dockerhub')]) {
                        sh "docker login -u razannadhif -p ${dockerhub}"
                    }
                    app.push("${env.BUILD_ID}")
                 }

            }
        }

        stage('Deploy to K8s') {
            steps{
                echo "Deployment started ..."
                sh 'ls -ltr'
                sh 'pwd'
                sh "sed -i 's/minpropokeapi:latest/minpropokeapi:${env.BUILD_ID}/g' deployment.yml"
                step([$class: 'KubernetesEngineBuilder', \
                  projectId: env.PROJECT_ID, \
                  clusterName: env.CLUSTER_NAME, \
                  location: env.LOCATION, \
                  manifestPattern: 'deployment.yml', \
                  credentialsId: env.CREDENTIALS_ID, \
                  verifyDeployments: true])
                }
            }
        }
}
