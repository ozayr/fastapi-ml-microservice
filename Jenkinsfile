pipeline{
    agent any 

    stages{
        stage('unit'){
            agent {
                docker {
                    image  'python:3.7-buster'
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
        stage(''){
            steps{
                echo 'welcome to the next stage'

            }


        }
    
    }

    post {
        cleanup {
            cleanWs()
        }
    }
}