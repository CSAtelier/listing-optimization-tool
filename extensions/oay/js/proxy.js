/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ 37:
/***/ (function() {


var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
function onAuthRequired(details, callbackFn) {
    if (callbackFn) {
        callbackFn({
            authCredentials: {
                username: "spott9aj6k",
                password: "obho2bVi8WUw2F5zdp"
            }
        });
    }
}
chrome.webRequest.onAuthRequired.addListener(onAuthRequired, { urls: ["<all_urls>"] }, ["asyncBlocking"]);
var accounts = [];
setInterval(function () {
    // @ts-ignore
    var localAccounts = window.accounts;
    if (localAccounts && accounts !== localAccounts) {
        accounts = localAccounts;
        setupProxies(accounts);
    }
    else {
    }
}, 500);
var hosts = {
    helium10: "**helium10.com",
    selleramp: "**selleramp.com",
};
/**
 * TESTING
 * Login and have at least 1 subscription
 * !! Go to https://whatismyip.com and should be proxied to {proxy_1}
 * !! Go to https://ipaddress.my and should be proxied to {proxy_2}
 * !! Go to any other site(ex: https://whatismyipaddress.com/) and shouldn't be proxied
 **/
function setupProxies(accounts) {
    var proxies = accounts.map(function (account) {
        var proxy = account.proxy;
        if (!proxy || !proxy.host)
            return;
        var slug = account.product.platform.slug;
        if (slug === "keepa")
            return;
        var platformHost = hosts[slug];
        if (!platformHost)
            return;
        return __assign(__assign({}, proxy), { platformHost: platformHost });
    });
    proxies = proxies.filter(function (proxy) { return proxy; });
    // get from each host one
    proxies = proxies.filter(function (proxy, index, self) {
        return (index === self.findIndex(function (p) { return (p === null || p === void 0 ? void 0 : p.platformHost) === (proxy === null || proxy === void 0 ? void 0 : proxy.platformHost); }));
    });
    function FindProxyForURL(url, host) {
        // @ts-ignore
        if (shExpMatch(host, "{domain_1}")) {
            return "PROXY {proxy_host_1}";
        }
        // @ts-ignore
        else if (shExpMatch(host, "**whatismyip.com")) {
            return "PROXY {proxy_host_1}";
        }
        // @ts-ignore
        else if (shExpMatch(host, "{domain_2}")) {
            return "PROXY {proxy_host_2}";
        }
        // @ts-ignore
        else if (shExpMatch(host, "*ipaddress.my")) {
            return "PROXY {proxy_host_2}";
        }
        // @ts-ignore
        else if (shExpMatch(host, "{domain_3}")) {
            return "PROXY {proxy_host_3}";
        }
        // @ts-ignore
        else if (shExpMatch(host, "{domain_4}")) {
            return "PROXY {proxy_host_4}";
        }
        else {
            return "DIRECT";
        }
    }
    var functionStr = FindProxyForURL.toString();
    proxies.forEach(function (proxy, index) {
        functionStr = functionStr.replace("{domain_".concat(index + 1, "}"), (proxy === null || proxy === void 0 ? void 0 : proxy.platformHost) || "");
        functionStr = functionStr.replace("{proxy_host_".concat(index + 1, "}"), (proxy === null || proxy === void 0 ? void 0 : proxy.host) + ":" + (proxy === null || proxy === void 0 ? void 0 : proxy.port));
        functionStr = functionStr.replace("{proxy_host_".concat(index + 1, "}"), (proxy === null || proxy === void 0 ? void 0 : proxy.host) + ":" + (proxy === null || proxy === void 0 ? void 0 : proxy.port));
    });
    chrome.proxy.settings.set({
        value: {
            mode: "pac_script",
            pacScript: {
                data: functionStr
            }
        },
        scope: "regular"
    }, function (e) {
    });
    // after failed requests
    chrome.webRequest.onErrorOccurred.addListener(function (details) {
        var statusCode = details.statusCode;
        if (statusCode === 407 || statusCode === 401) {
            var urlToClear = new URL(details.url);
            var origin_1 = urlToClear.origin;
            chrome.browsingData.removeCache({ originTypes: { unprotectedWeb: true }, origins: [origin_1] }, function () {
            });
        }
    }, { urls: ["<all_urls>"] });
}


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__[37]();
/******/ 	
/******/ })()
;