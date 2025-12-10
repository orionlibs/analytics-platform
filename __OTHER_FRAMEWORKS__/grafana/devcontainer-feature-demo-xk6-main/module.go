// Package base32 contains the grafana/devcontainer-feature-demo-xk6 demo k6 extension.
package base32

import (
	"encoding/base32"

	"github.com/grafana/sobek"
	"go.k6.io/k6/js/modules"
)

func init() {
	modules.Register("k6/x/base32", new(rootModule))
}

type rootModule struct{}

func (*rootModule) NewModuleInstance(vu modules.VU) modules.Instance {
	return &module{vu}
}

type module struct {
	vu modules.VU
}

func (m *module) Exports() modules.Exports {
	return modules.Exports{
		Named: map[string]any{
			"encode": m.encode,
			"decode": m.decode,
		},
	}
}

func (m *module) encode(data []byte) string {
	return base32.StdEncoding.EncodeToString(data)
}

func (m *module) decode(str string) (sobek.ArrayBuffer, error) {
	data, err := base32.StdEncoding.DecodeString(str)
	if err != nil {
		return sobek.ArrayBuffer{}, err
	}

	return m.vu.Runtime().NewArrayBuffer(data), nil
}

var (
	_ modules.Module   = (*rootModule)(nil)
	_ modules.Instance = (*module)(nil)
)
