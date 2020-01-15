DevBox on Spot
==============

DevBox on Spot is a small utility to run a development environment on spot instances on AWS.

## Dependencies

This project uses the python modules mentioned in [requirements.txt](requirements.txt). It also needs [jq](https://stedolan.github.io/jq/) for the `make connect` command.

## Usage

```bash
# Install required dependencies
make setup

# Build and deploy resource on AWS
make

# Start the instance
make start

# Check the status of the instance
make status

# Connect to the instance
make connect
```

To stop the instance, you can run the following command _within the instance_:

```bash
sudo shutdown -h now
```