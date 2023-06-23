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
    const username = event.queryStringParameters.username;
    const newPassword = event.queryStringParameters.new_password;
    const hashedPassword = await bcrypt.hash(newPassword, 10);

    return new Promise((resolve, reject) => {
        // First, get the user ID for later response
        pool.query('SELECT user_id FROM usuarios WHERE username = ?', [username], (error, results) => {
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
                const userId = results[0].user_id;

                // Now, update the password
                pool.query('UPDATE usuarios SET password = ? WHERE username = ?', [hashedPassword, username], (error, results) => {
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
                    } else {
                        resolve({
                            statusCode: 200,
                            headers: {
                                "Access-Control-Allow-Headers": "Content-Type",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                            },
                            body: JSON.stringify({ res: 'ok', id_user: userId })
                        });
                    }
                });
            }
        });
    });
};
