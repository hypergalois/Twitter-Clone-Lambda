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
    const user = event.queryStringParameters.user;
    const password = event.queryStringParameters.password;

    return new Promise((resolve, reject) => {
        pool.query('SELECT user_id, password FROM usuarios WHERE username = ?', [user], (error, results) => {
            if (error) {
                console.error(error);
                resolve({
                    statusCode: 500,
                    headers: {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                    body: JSON.stringify({ res: 'fail', user_id: null, error: 'serverError' })
                });
            } else if (results.length === 0) {
                resolve({
                    statusCode: 202,
                    headers: {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                    body: JSON.stringify({ res: 'fail', user_id: null, error: 'userNotExists' })
                });
            } else {
                const hashedPassword = results[0].password;
                const userId = results[0].user_id;

                bcrypt.compare(password, hashedPassword, (err, isMatch) => {
                    if (err) {
                        console.error(err);
                        resolve({
                            statusCode: 500,
                            headers: {
                                "Access-Control-Allow-Headers": "Content-Type",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                            },
                            body: JSON.stringify({ res: 'fail', user_id: null, error: 'serverError' })
                        });
                    } else if (!isMatch) {
                        resolve({
                            statusCode: 202,
                            headers: {
                                "Access-Control-Allow-Headers": "Content-Type",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                            },
                            body: JSON.stringify({ res: 'fail', user_id: null, error: 'passwordWrong' })
                        });
                    } else {
                        resolve({
                            statusCode: 200,
                            headers: {
                                "Access-Control-Allow-Headers": "Content-Type",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                            },
                            body: JSON.stringify({ res: 'ok', user_id: userId })
                        });
                    }
                });
            }
        });
    });
};