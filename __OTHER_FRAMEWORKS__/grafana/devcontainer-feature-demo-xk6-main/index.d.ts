/**
 * **Example k6 extension that implements base32 encoding.**
 *
 * @example
 * ```ts
 * import { randomBytes } from "k6/crypto"
 * import base32 from "k6/x/base32"
 *
 * export default function() {
 *   console.log(base32.encode(randomBytes(20)))
 * }
 * ```
 *
 * @module base32
 */
export as namespace base32;

/**
 * Encode binary data to a string using Base32 encoding.
 * 
 * @param data bytes to encode
 */
export declare function encode(data: ArrayBuffer): string;

/**
 * Decode binary data from a string using Base32 encoding.
 * 
 * @param str string to decode
 */
export declare function decode(str: string): ArrayBuffer;
