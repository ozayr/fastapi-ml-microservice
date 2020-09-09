pipeline{
    agent {docker {image  'python:3.7-alpine3.11'}}
    stages{
        // stage('checkout'){steps{
        //     git 'https://github.com/ozayr/fastapi-ml-microservice.git'
        // }}
        stage('setup'){
            steps{
                sh 'ls'
                sh 'python3 -m venv test_env'
                sh 'source test_env/bin/activate'
                sh 'sudo pip install --upgrade pip '
	            sh 'sudo pip install -r requirements.txt'
                sh 'sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64' 
		        sh 'sudo chmod +x /bin/hadolint'
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
    post { 
        always { 
           deleteDir()
        }
    }
}