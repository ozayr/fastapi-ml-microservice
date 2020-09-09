pipeline{
    agent {docker {image 'python:3.6.9'}}
    stages{
        // stage('checkout'){steps{
        //     git 'https://github.com/ozayr/fastapi-ml-microservice.git'
        // }}
        stage('setup'){
            steps{
                sh 'python -m venv test_env && source test_env/bin/activate'
                sh 'pip install --upgrade pip'
	            sh 'pip install -r requirements.txt'
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