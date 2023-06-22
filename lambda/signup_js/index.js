const mysql = require('mysql');
const bcrypt = require('bcryptjs');

const rds_host = process.env.rds_host
const usernameDB = process.env.usernameDB
const passwordDB = process.env.passwordDB
const dbname = process.env.dbname

const pool = mysql.createPool({
    connectionLimit: 10,
    host: rds_host,
    user: usernameDB,
    password: passwordDB,
    database: dbname
});

exports.handler = async (event, context) => {

    const nombre = event.queryStringParameters.nombre;
    const user = event.queryStringParameters.user;
    const email = event.queryStringParameters.email;
    const password = event.queryStringParameters.password;
    const frase = event.queryStringParameters.frase;

    const hashedPassword = await bcrypt.hash(password, 10);
    
    console.log(nombre, user, email, password, frase, hashedPassword)
    console.log(rds_host, usernameDB, passwordDB, dbname)

    return new Promise((resolve, reject) => {
        pool.query('SELECT * FROM usuarios WHERE username = ?', [user], (error, results) => {
            if (error) {
                console.error(error);
                resolve({
                    statusCode: 500,
                    headers: {
                        "Access-Control-Allow-Headers" : "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                    body: JSON.stringify({ res: 'fail', id_user: '', error: 'serverError' })
                });
            } else if (results.length > 0) {
                resolve({
                    statusCode: 400,
                    headers: {
                        "Access-Control-Allow-Headers" : "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                    body: JSON.stringify({ res: 'fail', id_user: '', error: 'userExists' })
                });
            } else {
                pool.query(
                    'INSERT INTO usuarios (name, username, email, password, recovery_phrase) VALUES (?, ?, ?, ?, ?)',
                    [nombre, user, email, hashedPassword, frase],
                    (error, results) => {
                        if (error) {
                            console.error(error);
                            resolve({
                                statusCode: 500,
                                headers: {
                                    "Access-Control-Allow-Headers" : "Content-Type",
                                    "Access-Control-Allow-Origin": "*",
                                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                                },
                                body: JSON.stringify({ res: 'fail', id_user: '', error: 'serverError' })
                            });
                        } else {
                            resolve({
                                statusCode: 200,
                                headers: {
                                    "Access-Control-Allow-Headers" : "Content-Type",
                                    "Access-Control-Allow-Origin": "*",
                                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                                },
                                body: JSON.stringify({ res: 'ok', id_user: results.insertId, error: ''})
                            });
                        }
                    }
                );
            }
        });
    });
};