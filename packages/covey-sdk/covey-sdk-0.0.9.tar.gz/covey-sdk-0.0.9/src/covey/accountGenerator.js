function generateNewAccounts(password, numberOfAccounts) {

    for (let index = 0; index < numberOfAccounts; index++) {
        const newAccount = personal.newAccount(password);
        console.log(newAccount);
    }
}
