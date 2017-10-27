window.applicationServerKey = '{{public_key}}';

window.addEventListener('subscribe', function (e) {
	return new Promise(function (resolve, reject) {
			const permissionResult = Notification.requestPermission(function (result) {
				resolve(result);
			});

			if (permissionResult) {
				permissionResult.then(resolve, reject);
			}
		})
		.then(function (permissionResult) {
			if (permissionResult !== 'granted') {
				throw new Error('We weren\'t granted permission.');
			} else {
				subscribe(e);
			}
		});
})

window.addEventListener('unsubscribe', function (e) {
	unsubscribe(e);
})

window.addEventListener('sendToSubscriber', function (e) {
	sendToSubscriber(e);
})

window.addEventListener('sendToSite', function (e) {
	sendToSite(e);
})

window.addEventListener('subscribesms', function (e) {
	sendSubscriptionToBackEnd(null, e.detail);
})

function urlB64ToUint8Array(base64String) {
	const padding = '='.repeat((4 - base64String.length % 4) % 4);
	const base64 = (base64String + padding)
		.replace(/\-/g, '+')
		.replace(/_/g, '/');

	const rawData = window.atob(base64);
	const outputArray = new Uint8Array(rawData.length);

	for (let i = 0; i < rawData.length; ++i) {
		outputArray[i] = rawData.charCodeAt(i);
	}
	return outputArray;
}

function unsubscribe(e) {
	if(!navigator.serviceWorker) {
		deleteSubscriptionFromBackEnd()
	}
	navigator.serviceWorker.ready.then(function (serviceWorkerRegistration) {
		serviceWorkerRegistration.pushManager.getSubscription().then(
			function (pushSubscription) {
				if (!pushSubscription) {
					deleteSubscriptionFromBackEnd()
					return
				}
				//remove from server;

				pushSubscription.unsubscribe().then(function () {
					deleteSubscriptionFromBackEnd()
				});
			})

	})
}

function subscribe(e) {
	if ('serviceWorker' in navigator) {
		navigator.serviceWorker.ready.then(function (serviceWorkerRegistration) {

			const subscribeOptions = {
				userVisibleOnly: true,
				applicationServerKey: urlB64ToUint8Array('{{public_key}}')
			};

			serviceWorkerRegistration.pushManager.subscribe(subscribeOptions).then(function (pushSub) {
				sendSubscriptionToBackEnd(pushSub, e.detail);
			})

		});

	}
}

function deleteSubscriptionFromBackEnd() {

	var token = '{{token}}';
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function () {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			window.dispatchEvent(new CustomEvent('unsubscribed', {
				detail: {status:xhr.status}
			}))
		}
	}
	xhr.open("DELETE", 'delete-opt-in', true);
	xhr.setRequestHeader('Authorization', 'Bearer ' + token);
	xhr.send(null);

}

function sendSubscriptionToBackEnd(subscription, payload) {
	var token = '{{token}}';
	if(!payload) {
		payload = {};
	}	
	if(subscription) {
		payload['webPushInfo'] = subscription;
	}
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function () {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			var id = 0;

			if(xhr.status === 200) {
				id = JSON.parse(xhr.responseText).payload.data.id;
			}

			window.dispatchEvent(new CustomEvent('subscribed', {
				detail: {status:xhr.status, id: id}
			}))
		}
	}
	xhr.open("POST", 'notification-opt-ins', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('Authorization', 'Bearer ' + token);
	xhr.send(JSON.stringify(payload));
}

function sendToSubscriber() {
	var token = '{{token}}';
	var xhr = new XMLHttpRequest();

	xhr.onreadystatechange = function () {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			window.dispatchEvent(new CustomEvent('sentToSubscriber', {
				detail: {status:xhr.status}
			}))
		}
	}

	xhr.open("POST", 'send-to-subscriber', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('Authorization', 'Bearer ' + token);
	xhr.send(null);
}

function sendToSite() {
	var token = '{{token}}';
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function () {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			window.dispatchEvent(new CustomEvent('sentToSubscriber', {
				detail: {status:xhr.status}
			}))
		}
	}

	xhr.open("POST", 'send-to-site', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('Authorization', 'Bearer ' + token);
	xhr.send();
}
