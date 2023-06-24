const CryptoJS = require("crypto-js");

function ofuscarNombreArchivo(nombreArchivo, clave) {
    var claveEnBytes = CryptoJS.enc.Utf8.parse(clave);
    var nombreArchivoEnBytes = CryptoJS.enc.Utf8.parse(nombreArchivo);
    
    var encrypted = CryptoJS.AES.encrypt(nombreArchivoEnBytes, claveEnBytes, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    
    return encrypted.toString();
}

function desofuscarNombreArchivo(nombreOfuscado, clave) {
    var claveEnBytes = CryptoJS.enc.Utf8.parse(clave);
    
    var decrypted = CryptoJS.AES.decrypt(nombreOfuscado, claveEnBytes, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    
    return decrypted.toString(CryptoJS.enc.Utf8);
}

let clave = 'unaclave'; // Se recomienda usar una clave segura

let nombreOriginal = Date.now() + 'archivo.txt';

// Ofuscar el nombre del archivo
let nombreOfuscado = ofuscarNombreArchivo(nombreOriginal, clave);

console.log('Nombre Ofuscado:', nombreOfuscado);

// Desofuscar el nombre del archivo
let nombreDesofuscado = desofuscarNombreArchivo(nombreOfuscado, clave);

console.log('Nombre Desofuscado:', nombreDesofuscado);


let nombreOriginal2 = '16876462208061687640099242Screenshot 2023-06-19 203243.png';

// Ofuscar el nombre del archivo
let nombreOfuscado2 = ofuscarNombreArchivo(nombreOriginal2, clave);

console.log('Nombre Ofuscado:', nombreOfuscado2);

// Desofuscar el nombre del archivo
let nombreDesofuscado2 = desofuscarNombreArchivo(nombreOfuscado2, clave);

console.log('Nombre Desofuscado:', nombreDesofuscado2);

MLoIRn4ujvqcJeh468poNwgUvRrY8/pLtaENw5KuQbQ2BKbjZaCNIpJ1HPMCgSK0cR+pNlciDz+c/B9a85oEug==