pipeline {
    agent any

    environment {
        IMAGE_NAME = "ramishaiftikhar/midterm-ml"
        CONTAINER_NAME = "midterm-ml-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build, Train & Test') {
            steps {
                script {
                    def sha = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.SHORT_SHA = sha
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                    sh """
                        docker run --rm \
                          -e GIT_COMMIT=${sha} \
                          -v "\$(pwd)/artifacts:/app/artifacts" \
                          ${IMAGE_NAME}:latest \
                          sh -c "python train.py && python -m unittest test_app.py"
                    """
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh """
                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      --restart unless-stopped \
                      -p 8000:8000 \
                      -v "\$(pwd)/artifacts:/app/artifacts" \
                      ${IMAGE_NAME}:latest
                """
                sh "sleep 3 && curl -f http://localhost:8000/health && curl -f http://localhost:8000/metrics"
            }
        }
    }

    post {
        always {
            script {
                def sha = env.SHORT_SHA ?: 'unknown'
                emailext(
                    to: 'qasimalik@gmail.com',
                    subject: "SP23-BAI-044 - Jenkins Build #${env.BUILD_NUMBER} (${currentBuild.currentResult})",
                    body: """Student Registration No: SP23-BAI-044
Build Status: ${currentBuild.currentResult}
Build Number: #${env.BUILD_NUMBER}
Git Commit SHA: ${sha}
Metrics Endpoint: http://13.63.148.66:8000/metrics
Build URL: ${env.BUILD_URL}"""
                )
            }
        }
    }
}
