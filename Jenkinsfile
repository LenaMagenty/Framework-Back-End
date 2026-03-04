pipeline {
    agent { label 'backend-agent' }

    stages {
        stage('Run tests') {
            steps {
                sh '''
                echo "Starting tests..."

                docker compose -f deploy/docker-compose.test.yml up --build --exit-code-from tests tests
                RESULT=$?

                echo "Containers status:"
                docker compose -f deploy/docker-compose.test.yml ps

                echo "AUTH SERVICE LOGS:"
                docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 auth

                echo "UNIVERSITY SERVICE LOGS:"
                docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 university

                echo "POSTGRES AUTH LOGS:"
                docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 postgres_auth

                echo "POSTGRES UNIVERSITY LOGS:"
                docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 postgres_university

                exit $RESULT
                '''
            }
        }
    }
}

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
        echo "Cleaning previous environment..."
        docker compose -f deploy/docker-compose.test.yml down -v || true

        echo "Starting tests..."
        docker compose -f deploy/docker-compose.test.yml up --build --exit-code-from tests tests
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