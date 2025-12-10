import { check } from "k6"
import { randomBytes } from "k6/crypto"
import base32 from "k6/x/base32"

export const options = {
    thresholds: {
        checks: ['rate==1'],
    },
};

function equals(ab1, ab2) {
    const a = new Uint8Array(ab1)
    const b = new Uint8Array(ab2)

    if (a.length != b.length) {
        return false
    }

    for (var i = 0; i < a.length; i++) {
        if (a[i] != b[i]) {
            return false
        }
    }

    return true
}

export default function () {
    const bytes = randomBytes(20)
    const encoded = base32.encode(bytes)

    console.log("encoded", encoded)

    check(encoded, {
        'decode(encode(x)) == x': (str) => equals(bytes, base32.decode(str))
    })
}
