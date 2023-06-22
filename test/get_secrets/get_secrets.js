const { SecretsManagerClient, GetSecretValueCommand } = require("@aws-sdk/client-secrets-manager")

const secretName = 'twitterdb'
const region = 'us-east-1'

const client = new SecretsManagerClient({ region })

async function getSecretValue() {
  try {
    const command = new GetSecretValueCommand({
      SecretId: secretName,
      VersionStage: 'AWSCURRENT'
    })

    const response = await client.send(command)
    const secret = response.SecretString

    console.log("Secret Value:", secret)

  } catch (error) {
    console.error("Error:", error)
  }
}

getSecretValue();