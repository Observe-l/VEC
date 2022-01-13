/*
 * Copyright IBM Corp All Rights Reserved
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric-chaincode-go/shim"
	"github.com/hyperledger/fabric-protos-go/peer"
)

// SimpleAsset implements a simple chaincode to manage an asset
type SimpleAsset struct {
}

// BaseStation's information
type BaseStation struct {
	ID                          string  `json:"id"`
	Global_computing_resource   float64 `json:"global_computing_resource"`
	Reversed_computing_resource float64 `json:"reversed_computing_resource"`
	Computing_efficiency        float64 `json:"computing_efficiency"`
	Completion_ratio            float64 `json:"completion_ratio"`
	Total_received_task         float64 `json:"total_received_task"`
	Reliability                 float64 `json:"reliability"`
}

// Init is called during chaincode instantiation to initialize any
// data. Note that chaincode upgrade also calls this function to reset
// or to migrate data.
func (t *SimpleAsset) Init(stub shim.ChaincodeStubInterface) peer.Response {
	// Get the args from the transaction proposal
	args := stub.GetStringArgs()
	if len(args) != 7 {
		return shim.Error("Incorrect arguments. Expecting a key and a value")
	}

	// Set up any variables or assets here by calling stub.PutState()
	ID := args[0]
	gres, err := strconv.ParseFloat(args[1], 64)
	if err != nil {
		return shim.Error("global_computing_resource input error")
	}
	rres, err := strconv.ParseFloat(args[2], 64)
	if err != nil {
		return shim.Error("reversed_computing_resource input error")
	}
	eff, err := strconv.ParseFloat(args[3], 64)
	if err != nil {
		return shim.Error("computing_efficiency input error")
	}
	rat, err := strconv.ParseFloat(args[4], 64)
	if err != nil {
		return shim.Error("completion_ratio input error")
	}
	total, err := strconv.ParseFloat(args[5], 64)
	if err != nil {
		return shim.Error("total_received_task input error")
	}
	rel, err := strconv.ParseFloat(args[6], 64)
	if err != nil {
		return shim.Error("reliability input error")
	}

	// Create Basestation object and marshal to JSON
	basestation := &BaseStation{ID, gres, rres, eff, rat, total, rel}
	bsJSONasBytes, err := json.Marshal(basestation)
	if err != nil {
		return shim.Error(err.Error())
	}

	// Save data on the ledger
	err = stub.PutState(ID, bsJSONasBytes)
	if err != nil {
		return shim.Error(fmt.Sprintf("Failed to create asset: %s", args[0]))
	}
	return shim.Success([]byte(args[0]))
}

// Invoke is called per transaction on the chaincode. Each transaction is
// either a 'get' or a 'set' on the asset created by Init function. The Set
// method may create a new asset by specifying a new key-value pair.
func (t *SimpleAsset) Invoke(stub shim.ChaincodeStubInterface) peer.Response {
	// Extract the function and args from the transaction proposal
	fn, args := stub.GetFunctionAndParameters()
	if fn == "set" {
		return t.set(stub, args)
	} else if fn == "del" {
		return t.del(stub, args)
	} else if fn == "mul_get" {
		return t.mul_get(stub, args)
	} else { // assume 'get' even if fn is nil
		return t.get(stub, args)
	}
}

// Set stores the asset (both key and value) on the ledger. If the key exists,
// it will override the value with the new one
func (t *SimpleAsset) set(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	if len(args) != 7 {
		return shim.Error("Incorrect arguments. Expecting a key and a value")
	}

	ID := args[0]
	gres, err := strconv.ParseFloat(args[1], 64)
	if err != nil {
		return shim.Error("Global_computing_resource input error")
	}
	rres, err := strconv.ParseFloat(args[2], 64)
	if err != nil {
		return shim.Error("Reversed_computing_resource input error")
	}
	eff, err := strconv.ParseFloat(args[3], 64)
	if err != nil {
		return shim.Error("Computing_efficiency input error")
	}
	rat, err := strconv.ParseFloat(args[4], 64)
	if err != nil {
		return shim.Error("Completion_ratio input error")
	}
	total, err := strconv.ParseFloat(args[5], 64)
	if err != nil {
		return shim.Error("Total_received_task input error")
	}
	rel, err := strconv.ParseFloat(args[6], 64)
	if err != nil {
		return shim.Error("Reliability input error")
	}

	// Create Basestation object and marshal to JSON
	basestation := &BaseStation{ID, gres, rres, eff, rat, total, rel}
	bsJSONasBytes, err := json.Marshal(basestation)
	if err != nil {
		return shim.Error(err.Error())
	}

	// Save data on the ledger
	err = stub.PutState(ID, bsJSONasBytes)

	if err != nil {
		return shim.Error(err.Error())
	}
	fmt.Println("Successful set state of Base Station" + args[0])
	return shim.Success(nil)
}

// delete a data
func (t *SimpleAsset) del(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	var jsonResp string
	if len(args) != 1 {
		return shim.Error("Incorrect arguments. Expecting a key")
	}

	err := stub.DelState(args[0])
	if err != nil {
		jsonResp = "{\"Error\":\"Failed to delete the state of Base Station" + args[0] + "\"}"
		return shim.Error(jsonResp)
	}
	fmt.Println("Successful delete the state of Base Station" + args[0])
	return shim.Success(nil)
}

// Get returns the value of the specified asset key
func (t *SimpleAsset) get(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	var jsonResp string
	if len(args) != 1 {
		return shim.Error("Incorrect arguments. Expecting a key")
	}

	value, err := stub.GetState(args[0])
	if err != nil {
		jsonResp = "{\"Error\":\"Failed to get the state of Base Station: " + args[0] + "\"}"
		return shim.Error(jsonResp)
	}
	if value == nil {
		jsonResp = "{\"Error\":\"Base Station does not exist " + args[0] + "\"}"
		return shim.Error(jsonResp)
	}
	return shim.Success(value)
}

// mul_get returns all of data in a json format
func (t *SimpleAsset) mul_get(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	var assets bytes.Buffer
	bAlreadyWritten := false

	assets.WriteString("[")
	for i := 0; i < len(args); i++ {
		value, err := stub.GetState(args[i])
		if err != nil {
			return shim.Error("Failed to get state:" + args[i] + " with error: " + err.Error())
		}
		if value == nil {
			return shim.Error("State not found: " + args[i])
		}
		if bAlreadyWritten {
			assets.WriteString(",")
		}
		assets.WriteString("{\"id\":")
		assets.WriteString("\"")
		assets.WriteString(args[i])
		assets.WriteString("\"")

		assets.WriteString(", \"Record\":")
		assets.Write(value)
		assets.WriteString("}")
		bAlreadyWritten = true
	}
	assets.WriteString("]")

	return shim.Success(assets.Bytes())
}

// main function starts up the chaincode in the container during instantiate
func main() {
	if err := shim.Start(new(SimpleAsset)); err != nil {
		fmt.Printf("Error starting SimpleAsset chaincode: %s", err)
	}
}
