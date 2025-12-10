namespace smithy.example

use smithy.waiters#waitable

@waitable(
    thingNotExists: {
        "documentation": "Something",
        "acceptors": [
            {
                "state": "success",
                "matcher": {
                    "output": {
                        "path": "baz == 'hi'",
                        "comparator": "booleanEquals",
                        "expected": "true"
                    }
                }
            }
        ]
    }
)
operation A {
    output: AOutput,
}

structure AOutput {
    baz: String,
}
