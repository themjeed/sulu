
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Getting latest source code'
                checkout scm
                bat 'git log -1 --oneline'
            }
        }

        stage('Check Requirements') {
            steps {
                bat '''
                if exist requirements.txt (
                    echo Requirements file found
                    type requirements.txt
                ) else (
                    echo requirements.txt not found
                )
                '''
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker --version'
                bat 'docker compose version'
            }
        }

        stage('Build') {
            steps {
                script {
                    if (fileExists('docker-compose.yml')) {
                        bat 'docker compose config'
                        bat 'docker compose build'
                    }
                    else if (fileExists('compose.yaml')) {
                        bat 'docker compose -f compose.yaml config'
                        bat 'docker compose -f compose.yaml build'
                    }
                    else if (fileExists('Dockerfile')) {
                        bat 'docker build -t my-application:latest .'
                    }
                    else {
                        error('No Docker build file found')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (fileExists('docker-compose.yml')) {
                        bat 'docker compose up -d'
                    }
                    else if (fileExists('compose.yaml')) {
                        bat 'docker compose -f compose.yaml up -d'
                    }
                    else {
                        echo 'Dockerfile only: image built, no Compose deployment'
                    }
                }
            }
        }

        stage('Check Containers') {
            steps {
                bat 'docker ps'
            }
        }
    }

    post {
        success {
            echo 'Application deployed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
