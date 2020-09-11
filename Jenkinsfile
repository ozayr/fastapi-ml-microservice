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
            stages{
                stage('build  image'){
                    steps{
                        sh 'docker build --tag=ozayr0116/ml_microservice .' 
                        sh 'docker image ls'
                    }
                }
                stage('run and test API'){
                    steps{
                        sh 'docker run --rm -d -p 8000:8000 --name image_test ozayr0116/ml_microservice'   
                        sh 'sleep 5'
                        script {
                            final String response = sh(script: 'curl http://localhost:8000/api/status', returnStdout: true).trim()
                            echo response
                        }
                    }
                }

                stage('load test'){
                    steps{
                        sh 'locust -f load_tests/locustfile.py --headless -u 100 -r 100 --run-time 10s  --host=http://localhost:8000' 
                        sh 'docker container stop image_test'
                
                    }
                stage('upload image'){
                    steps{
                        sh 'docker push ozayr0116/ml_microservice:latest'
                    }
                    
                }

                }
                    post{
                        failure{
                            sh 'docker container stop $(docker ps -a -q)'
                        }
                    }

                }
            }
        }
    
    }

    post {
        cleanup {
            cleanWs()
        }
    }
}