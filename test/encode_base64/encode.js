const parameters = {
    id_user: 3
}

// Convertir objeto a JSON y codificarlo base64
const encodedParams = btoa(JSON.stringify(parameters))

console.log(encodedParams)