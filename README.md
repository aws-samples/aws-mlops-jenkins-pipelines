# ML Pipelines with AWS Glue and Amazon SageMaker using Jenkins

In this repository we are stepping through the implementation of a CI/CD ML pipeline using AWS Glue for data processing, Amazon SageMaker for training, versioning, and hosting Real-Time endpoints, and Jenkins CI/CD pipelines for orchestrating the Workflow.
Through the usage of [AWS CLI APIs for SageMaker](https://docs.aws.amazon.com/cli/latest/reference/sagemaker/), and [AWS CLI APIs for AWS Glue](https://docs.aws.amazon.com/cli/latest/reference/glue/index.html)
we are showing how to implement CI/CD ML pipelines for processing data using [AWS Glue](https://docs.aws.amazon.com/glue/index.html), 
training ML models using [Amazon SageMaker Training](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html),
deploying ML models using [Amazon SageMaker Hosting Services](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html), 
or perform batch inference by using [Amazon SageMaker Batch Transform](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html).

Everything can be tested by using the following frameworks:
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/sagemaker/)
* [Amazon SageMaker DeepAR](https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html)
* [Jenkins](https://www.jenkins.io/)

## Reference Architecture

![Alt text](docs/architecture.png?raw=true "Architecture")

## Training pipeline

![Alt text](docs/train.png?raw=true "Training Pipeline")

## Deployment pipeline

![Alt text](docs/deployment.png?raw=true "Deployment Pipeline")

## Environment Setup

Setup the ML environment by deploying the [CloudFormation](./infrastructure_templates) templates described as below:

1.[00-ml-environment](./infrastructure_templates/00-ml-environment.yml): This template is deploying the necessary resources 
for the Amazon SageMaker Resources, such as Amazon KMS Key and Alias, Amazon S3 Bucket for storing code and ML model artifacts, 
Amazon SageMaker Model Registry for versioning ML models, IAM policies and roles for Amazon SageMaker and for Jenkins AWS Profile.
*Parameters*:
  * KMSAlias: Name of the the KMS alias. *Optional*
  * ModelPackageGroupDescription: Description for the Amazon SageMaker Model Package Group. *Optional*
  * ModelPackageGroupName: Name for the Amazon SageMaker Model Package Group. *Mandatory*
  * S3BucketName: Amazon S3 Bucket name. *Mandatory*

## Source Code

### Build and Train ML models

* [ml-build-train/algorithms](source_code/00-ml-build-train/algorithms): This folder contains the scripts necessary for performing data processing
  * [ml-build-train/algorithms/processing-glue](source_code/00-ml-build-train/algorithms/processing-glue): This folder contains the Python scripts for processing data
  * [ml-build-train/algorithms/processing-glue-spark](source_code/00-ml-build-train/algorithms/processing-glue-spark): This folder contains the Python scripts for processing data by using
  Spark with Python (PySpark)
* [ml-build-train/mlpipelines](source_code/00-ml-build-train/mlpipelines)
  * [ml-build-train/mlpipelines/training](source_code/00-ml-build-train/mlpipelines/training/Jenkinsfile): This is a Jenkinsfile example to be used for creating 
  the Jenkins Pipeline for training

### Inference and Deploy ML models

* [ml-inference-deploy/mlpipelines](source_code/01-ml-inference-deploy/mlpipelines)
  * [ml-inference-deploy/mlpipelines/deploy](source_code/01-ml-inference-deploy/mlpipelines/deploy/Jenkinsfile): This is a Jenkinsfile example to be used for creating 
  the Jenkins Pipeline for deploying Amazon SageMaker Endpoints by using the latest approved model taken from the Amazon SageMaker 
  Model Registry
  * [ml-inference-deploy/mlpipelines/inference](source_code/01-ml-inference-deploy/mlpipelines/inference/Jenkinsfile): This is a Jenkinsfile example to be used for creating 
  the Jenkins Pipeline for running a batch inference job by using Amazon SageMaker Batch Transform by using the latest approved model taken from the Amazon SageMaker 
  Model Registry

## Jenkins Environment

In this section, we are setting up a local Jenkins environment for testing the ML pipelines. Please follow the [README](./jenkins/README.md) 
for running Jenkins by using the provided Dockerfile in a container.

### Setup pipeline

For creating the Jenkins Pipeline:

#### Create Job

![Alt text](docs/create-job.png?raw=true "Create Job")

#### Create Pipeline

![Alt text](docs/create-job.png?raw=true "Create Pipeline")

#### Define Jenkinsfile

Create a Jenkins pipeline for the specific purpose by copying the content from 

* [ml-build-train/mlpipelines/training](source_code/00-ml-build-train/mlpipelines/training/Jenkinsfile)
* [ml-inference-deploy/mlpipelines/deploy](source_code/01-ml-inference-deploy/mlpipelines/deploy/Jenkinsfile)
* [ml-inference-deploy/mlpipelines/deploy](source_code/01-ml-inference-deploy/mlpipelines/inference/Jenkinsfile)

![Alt text](docs/training-pipeline-jenkins.png?raw=true "Define Jenkinsfile")

#### Define Jenkinsfile from Git repository

Create a Jenkins pipeline by pointing to a Jenkinsfile directly from the Git repository:

training-pipeline-github

![Alt text](docs/training-pipeline-github.png?raw=true "Create Pipeline Git")

## Conclusion

In this example we shared how to implement end to end pipelines for Machine Learning workloads using Jenkins, by using APIs with 
[AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/) for interacting with AWS Glue, Amazon SageMaker for processing, training, and [versioning ML models](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html),
for creating real-time endpoints or perform batch inference using Amazon SageMaker.

If you have any comments, please contact:

Bruno Pistone <bpistone@amazon.com>

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

