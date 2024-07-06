#!/bin/bash

# Generate the plan and save it to a file
terraform plan -out=plan.tfplan

# Output the plan in text format
terraform show -no-color plan.tfplan > plan.txt

echo "Terraform plan saved in plan.txt"
