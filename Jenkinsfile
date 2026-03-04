pipeline {
  agent { label 'backend-agent' }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Run tests in docker compose') {
      steps {
        sh '''
          docker-compose -f deploy/docker-compose.test.yml up --build --exit-code-from tests tests
        '''
      }
    }
  }

  post {
    always {
      sh '''
        docker-compose -f deploy/docker-compose.test.yml down -v --remove-orphans || true
      '''
    }
  }
}