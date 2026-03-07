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
                docker compose -f CI-CD/docker-compose.test.yml down -v --remove-orphans || true
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                set +e
                mkdir -p ${WORKSPACE}/allure-results
                echo "Starting tests..."
                docker compose -f CI-CD/docker-compose.test.yml up --build --exit-code-from tests tests
                RESULT=$?

                echo "Compose exit code: $RESULT"

                echo "Copying allure results from container..."
                docker cp backend-tests:/app/allure-results/. ${WORKSPACE}/allure-results/ || true

                exit $RESULT
                '''
            }
        }

        stage('Deploy') {
            environment {
                POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
            }
            steps {
                sh '''
                cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB_AUTH=auth
POSTGRES_DB_UNIVERSITY=university
AUTH_SERVICE_INTERNAL_URL=http://auth:8000
AUTH_SERVICE_API_URL=http://127.0.0.1:8000
UNIVERSITY_SERVICE_INTERNAL_URL=http://university:8000
UNIVERSITY_SERVICE_API_URL=http://127.0.0.1:8001
EOF
                docker compose -f docker-compose.yml up -d --pull always
                '''
            }
        }
    }

    post {
        always {
            sh '''
            set +e

            echo "Containers status:"
            docker compose -f CI-CD/docker-compose.test.yml ps || true

            echo "AUTH SERVICE LOGS:"
            docker compose -f CI-CD/docker-compose.test.yml logs --no-color --tail=200 auth || true

            echo "UNIVERSITY SERVICE LOGS:"
            docker compose -f CI-CD/docker-compose.test.yml logs --no-color --tail=200 university || true

            echo "POSTGRES AUTH LOGS:"
            docker compose -f CI-CD/docker-compose.test.yml logs --no-color --tail=200 postgres_auth || true

            echo "POSTGRES UNIVERSITY LOGS:"
            docker compose -f CI-CD/docker-compose.test.yml logs --no-color --tail=200 postgres_university || true

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
            docker compose -f CI-CD/docker-compose.test.yml down -v --remove-orphans || true
            '''
        }
    }
}