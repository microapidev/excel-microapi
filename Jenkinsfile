//This  is the Jenkinsfile for the excel-paser.

pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Git') {
            steps {
                echo '> Checking out the Git version control ...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo '>  Building the Docker images and starting the docker containers ...'
                sh 'docker-compose up'
            }
            post {
                failure {
                    echo 'This build has failed. See logs for details.'
                }
            }
        }
        stage('Testing') {
            steps {
                echo '> Running unit testing ...'
                sh 'docker-compose exec app python manage.py test '
            }
        }
        post {
            failure {
                echo 'This test has failed. See logs for details.'
            }
            success {
                echo 'Test passed'
            }
        }
    }
}
