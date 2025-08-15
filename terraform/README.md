# Terraform Infrastructure Setup

This directory contains the Terraform configuration files for setting up the infrastructure required for the data pipeline project.

## Overview

The Terraform setup will create the necessary resources for the project, including:

- PostgreSQL database
- Datasets for silver and gold layers

## Getting Started

To deploy the infrastructure, follow these steps:

1. **Install Terraform**: Ensure you have Terraform installed on your machine. You can download it from [terraform.io](https://www.terraform.io/downloads.html).

2. **Configure Variables**: Update the `variables.tf` file with your specific configurations, such as database credentials and dataset names.

3. **Initialize Terraform**: Run the following command to initialize the Terraform configuration:

   ```
   terraform init
   ```

4. **Plan the Deployment**: Use the following command to see what resources will be created:

   ```
   terraform plan
   ```

5. **Apply the Configuration**: To create the resources, run:

   ```
   terraform apply
   ```

   Confirm the action when prompted.

## Important Notes

- The infrastructure setup for datasets (silver and gold) will only occur if they do not already exist. If the datasets are already present, Terraform will skip their creation.

- Ensure that you have the necessary permissions to create resources in your cloud provider.

## Cleanup

To remove the created resources, you can run:

```
terraform destroy
```

This command will delete all resources defined in your Terraform configuration.