pipeline {
  agent { label 'backend-agent' }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'develop',
            url: 'https://github.com/LenaMagenty/Framework-Back-End.git'
      }
    }

    stage('Run tests') {
      steps {
        sh '''
        docker compose -f deploy/docker-compose.test.yml up \
          --build \
          --exit-code-from tests tests
        '''
      }
    }

  }

  post {
    always {
      sh '''
      docker compose -f deploy/docker-compose.test.yml down -v || true
      '''
    }
  }
}