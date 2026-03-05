pipeline {
    agent { label 'backend-agent' }

    options {
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

            echo "Workspace contents (for debugging):"
            ls -la || true
            ls -la allure-results || true

            echo "Allure results files:"
            find allure-results -maxdepth 2 -type f | head -n 50 || true
            '''

            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])

            sh '''
            echo "Final cleanup..."
            docker compose -f deploy/docker-compose.test.yml down -v --remove-orphans || true
            '''
        }
    }
}