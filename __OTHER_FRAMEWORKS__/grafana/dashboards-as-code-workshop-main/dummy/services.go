package main

import (
	"net/http"
)

var services = []Service{
	{
		Name:    "users",
		Version: "v1.2.3",
		HTTP: []HTTPEndpoint{
			{
				Method:  http.MethodPost,
				Code:    http.StatusOK,
				Path:    "/api/users/authenticate",
				Count:   [2]int{2, 7},
				Latency: [2]int{15, 45},
			},
			{
				Method:  http.MethodPost,
				Code:    http.StatusUnauthorized,
				Path:    "/api/users/authenticate",
				Count:   [2]int{0, 3},
				Latency: [2]int{10, 25},
			},
			{
				Method:  http.MethodPost,
				Code:    http.StatusOK,
				Path:    "/api/users/profile",
				Count:   [2]int{1, 3},
				Latency: [2]int{20, 55},
			},
		},
		GRPC: []GRPCEndpoint{
			{
				Service: "grpc.UsersService",
				Method:  "getProfile",
				Code:    "OK",
				Count:   [2]int{1, 3},
				Latency: [2]int{15, 55},
			},
		},
	},
	{
		Name:    "payments",
		Version: "v2.0.1",
		HTTP: []HTTPEndpoint{
			{
				Method:  http.MethodPost,
				Code:    http.StatusOK,
				Path:    "/api/payments",
				Count:   [2]int{0, 5},
				Latency: [2]int{200, 550},
			},
			{
				Method:  http.MethodPost,
				Code:    http.StatusTeapot,
				Path:    "/api/payments",
				Count:   [2]int{0, 1},
				Latency: [2]int{42, 42},
			},
		},
	},
	{
		Name:    "orders",
		Version: "v1.24.42",
		HTTP: []HTTPEndpoint{
			{
				Method:  http.MethodGet,
				Code:    http.StatusOK,
				Path:    "/api/orders/{order_ref}",
				Count:   [2]int{4, 9},
				Latency: [2]int{100, 350},
			},
			{
				Method:  http.MethodPost,
				Code:    http.StatusOK,
				Path:    "/api/orders",
				Count:   [2]int{1, 3},
				Latency: [2]int{350, 650},
			},
		},
	},
	{
		Name:    "products",
		Version: "v3.6.9",
		HTTP: []HTTPEndpoint{
			{
				Method:  http.MethodGet,
				Code:    http.StatusOK,
				Path:    "/api/products",
				Count:   [2]int{1, 20},
				Latency: [2]int{50, 1_000},
			},
			{
				Method:  http.MethodGet,
				Code:    http.StatusOK,
				Path:    "/api/products/{product_id}",
				Count:   [2]int{0, 10},
				Latency: [2]int{30, 900},
			},
			{
				Method:  http.MethodGet,
				Code:    http.StatusOK,
				Path:    "/api/products/{product_id}/reviews",
				Count:   [2]int{0, 8},
				Latency: [2]int{90, 1_400},
			},
			{
				Method:  http.MethodPost,
				Code:    http.StatusNotFound,
				Path:    "/api/products/{product_id}",
				Count:   [2]int{0, 2},
				Latency: [2]int{5, 10},
			},
		},
		GRPC: []GRPCEndpoint{
			{
				Service: "grpc.ProductService",
				Method:  "updateProductDetails",
				Code:    "OK",
				Count:   [2]int{1, 3},
				Latency: [2]int{15, 55},
			},
			{
				Service: "grpc.ProductService",
				Method:  "updateProductStock",
				Code:    "OK",
				Count:   [2]int{1, 10},
				Latency: [2]int{5, 25},
			},
			{
				Service: "grpc.ProductService",
				Method:  "updateProductStock",
				Code:    "InvalidArgument",
				Count:   [2]int{0, 8},
				Latency: [2]int{5, 25},
			},
		},
	},
}
