pipeline{
    agent any 
    environment{
        ORGANISATION = 'ozayr0116'
    }
    stages{
        stage('src test'){
            agent {
                docker {
                    image  'python:3.7-buster'
                    args '--user 0:0'}}

            stages{
                stage('setup'){
                    steps{
                        // sh 'python3 -m venv test_env'
                        // sh 'source test_env/bin/activate'
                        
                        // withEnv(['HOME=${env.WORKSPACE}']) {
                        sh 'pip install --upgrade pip'
                        sh 'pip install -r requirements_test.txt'
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

            }}

        stage('image test'){
            stages{

                stage('build  image'){
                    steps{
                        sh 'docker build --tag=${ORGANISATION}/${JOB_NAME}:${BUILD_NUMBER} .' 
                        sh 'docker image ls'}}

                stage('run and test API'){
                    steps{
                        sh 'docker run --rm -d -p 8000:8000 --name image_test ${ORGANISATION}/${JOB_NAME}:${BUILD_NUMBER}'   
                        sh 'sleep 5'
                        script {
                            final String response = sh(script: 'curl http://localhost:8000/api/status', returnStdout: true).trim()
                            echo response
                        }
                        sh 'docker container stop image_test'}

                    post{
                    failure{
                        sh 'docker container stop $(docker ps -a -q)'}}}

                stage('upload image'){
                    steps{
                        withCredentials([usernamePassword(credentialsId: 'docker-login', passwordVariable: 'pass', usernameVariable: 'user')]) {
                            sh 'docker login -u ${user} -p ${pass}'
                            sh 'docker tag ${ORGANISATION}/${JOB_NAME}:${BUILD_NUMBER} ${ORGANISATION}/${JOB_NAME}:latest'
                            sh 'docker push ${ORGANISATION}/${JOB_NAME}:latest'
                            sh 'docker push ${ORGANISATION}/${JOB_NAME}:${BUILD_NUMBER}'}}}
            }}

        stage('deploy'){
            steps{
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: '55b1102a-33af-4b8f-95a0-14ec04c80e47', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script{
                        cluster = sh(script: 'aws eks list-clusters --query "clusters[*]" --output=text', returnStdout: true).trim()
                        
                        if(cluster.isEmpty()){
                            sh 'sed "s/JOB_NAME/${JOB_NAME}/g" deployment/cluster.yml'
                            sh 'eksctl create cluster -f deployment/cluster.yml'
                            sh 'kubectl create -f loadbalancer.yaml'
                        }
                    }   
                    sh 'sed "s/JOB_NAME/${JOB_NAME}/g" deployment/deployment.yml'
                    sh 'sed "s/BUILD_NUM/${BUILD_NUMBER}/g" deployment/deployment.yml'
                    sh 'sed "s/ORGANISATION/${ORGANISATION}/g" deployment/deployment.yml'

                    sh 'kubectl -f apply deployment/deployment.yml'
                    sh 'kubectl rollout status deployment.v1.apps/${JOB_NAME}-app'
                    
                    // load_balancer_ip = sh()
                    // slackSend channel:'#levelup',
                    //             message:'load balancer IP ${load_balancer_ip}'
                    
                        
                    }}

        post{
            failure{
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: '55b1102a-33af-4b8f-95a0-14ec04c80e47', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                sh 'kubectl rollout undo deployment.v1.apps/${JOB_NAME}-app'
            }}
        }}


    }

    post {
        cleanup {
            cleanWs()}
        

}}
