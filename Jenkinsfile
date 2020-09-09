pipeline{
    agent any
    stages{
        // stage('checkout'){steps{
        //     git 'https://github.com/ozayr/fastapi-ml-microservice.git'
        // }}
        stage('setup'){
            steps{
                sh 'python3 -m venv test_env && source test_env/bin/activate'
        }}
        stage('lint'){
            steps{
                hadolint Dockerfile;
	            sh 'pylint --ignore=tests --disable=R,C,W1203,E0611 api'
        }}
        stage('test'){
            steps{
                sh 'pytest'
        }}
        // stage(){steps{}}
    }
}