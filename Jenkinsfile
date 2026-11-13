
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Tools') {
            steps {
                bat 'python --version'
                bat 'docker --version'
                bat 'docker compose version'
            }
        }

        stage('Detect Application') {
            steps {
                bat 'python detect.py'
            }
        }

        stage('Generate Docker Files') {
            steps {
                bat 'python generate.py'
            }
        }

        stage('Validate Compose') {
            steps {
                bat 'docker compose -p sulu-auto -f docker-compose.generated.yml config'
            }
        }

        stage('Build Images') {
            steps {
                bat 'docker compose -p sulu-auto -f docker-compose.generated.yml build'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker compose -p sulu-auto -f docker-compose.generated.yml up -d --remove-orphans'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker compose -p sulu-auto -f docker-compose.generated.yml ps'
                bat 'docker ps'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Application deployed successfully!'
            echo 'Check application at http://localhost:5002'
        }

        failure {
            echo 'ERROR: Pipeline failed. Check the Jenkins Console Output.'
        }
    }
}
