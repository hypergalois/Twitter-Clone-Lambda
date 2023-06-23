const mysql = require('mysql');

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
    const username = event.queryStringParameters.username;
    const recoveryPhrase = event.queryStringParameters.recovery_phrase;

    return new Promise((resolve, reject) => {
        pool.query('SELECT recovery_phrase FROM usuarios WHERE username = ?', [username], (error, results) => {
            if (error) {
                console.error(error);
                resolve({
                    statusCode: 500,
                    headers: {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                    body: JSON.stringify({ res: 'fail', error: 'serverError' })
                });
            } else if (results.length === 0) {
                resolve({
                    statusCode: 404,
                    headers: {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                    body: JSON.stringify({ res: 'fail', error: 'userNotFound' })
                });
            } else {
                const storedRecoveryPhrase = results[0].recovery_phrase;

                if (recoveryPhrase === storedRecoveryPhrase) {
                    resolve({
                        statusCode: 200,
                        headers: {
                            "Access-Control-Allow-Headers": "Content-Type",
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                        },
                        body: JSON.stringify({ res: 'ok' })
                    });
                } else {
                    resolve({
                        statusCode: 403,
                        headers: {
                            "Access-Control-Allow-Headers": "Content-Type",
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                        },
                        body: JSON.stringify({ res: 'fail', error: 'invalidRecoveryPhrase' })
                    });
                }
            }
        });
    });
};
