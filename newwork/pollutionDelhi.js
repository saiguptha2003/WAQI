var requestOptions = {
  method: 'GET',
  redirect: 'follow'
};
const STATE_NAME='delhi';
const YOUR_API_KRY='eccd8462-e32a-4676-8766-37990da282d5'
const COUNTRY_NAME='india';
fetch("https://api.waqi.info/feed/here/?token=6adbc6ff13fe01a446ff9fb49c7d993d69d71fe3", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));