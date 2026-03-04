pipeline {
    agent { label 'backend-agent' }

    options {
        // чтобы билды не дрались за docker/volumes/порты
        disableConcurrentBuilds(abortPrevious: true)
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/develop']],
                    userRemoteConfigs: [[url: 'https://github.com/LenaMagenty/Framework-Back-End.git']]
                ])
            }
        }

        stage('Cleanup before') {
            steps {
                sh '''
                echo "Cleaning previous environment..."
                docker compose -f deploy/docker-compose.test.yml down -v --remove-orphans || true
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                set +e

                echo "Starting tests..."
                docker compose -f deploy/docker-compose.test.yml up --build --exit-code-from tests tests
                RESULT=$?

                echo "Compose exit code: $RESULT"
                exit $RESULT
                '''
            }
        }
    }

    post {
        always {
            sh '''
            set +e

            echo "Containers status:"
            docker compose -f deploy/docker-compose.test.yml ps || true

            echo "AUTH SERVICE LOGS:"
            docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 auth || true

            echo "UNIVERSITY SERVICE LOGS:"
            docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 university || true

            echo "POSTGRES AUTH LOGS:"
            docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 postgres_auth || true

            echo "POSTGRES UNIVERSITY LOGS:"
            docker compose -f deploy/docker-compose.test.yml logs --no-color --tail=200 postgres_university || true

            echo "Final cleanup..."
            docker compose -f deploy/docker-compose.test.yml down -v --remove-orphans || true
            '''
        }
    }
}