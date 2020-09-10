pipeline{
    agent any 

    stages{
        stage('src test'){
            agent {
                docker {
                    image  'python:3.8.5-buster'
                    args '--user 0:0'
                    }
                }
            stages{
                stage('setup'){
                    steps{
                        // sh 'python3 -m venv test_env'
                        // sh 'source test_env/bin/activate'
                        
                        // withEnv(['HOME=${env.WORKSPACE}']) {
                        sh 'pip install --upgrade pip'
                        sh 'pip install -r requirements.txt'
                        //  python stuff
                        // }
                        sh 'wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64' 
                        sh 'chmod +x /bin/hadolint'     
                }}
                stage('lint'){
                    steps{
                        sh 'hadolint Dockerfile'
                        sh 'pylint --ignore=tests --disable=R,C,W1203,E0611 api'
                }}
                stage('test'){
                    steps{
                        sh 'pytest'
                }}
                // stage(){steps{}}
            }
        }
        stage('image test'){
            steps{
                sh 'docker build --tag=ozayr0116/ml_microservice .' 
                sh 'docker image ls'
                sh 'docker run --rm -d -p 8000:8000 --name image_test ozayr0116/ml_microservice'   
                sh 'sleep 5'
                script {
                    final String response = sh(script: 'curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"data\":[[0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98]]}"', returnStdout: true).trim()
                    echo response
                }
                sh 'docker container stop image_test'
            }
        }
    
    }

    post {
        cleanup {
            cleanWs()
        }
        always{
            sh 'docker container stop $(docker ps -a -q)'
            
        }
    }
}