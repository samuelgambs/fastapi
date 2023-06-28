pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t myapp .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run myapp pytest'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 8000:8000 myapp'
            }
        }
    }
}
