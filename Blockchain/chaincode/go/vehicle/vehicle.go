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
type Vehicle struct {
	ID                                          string  `json:"id"`
	RATIO                         				float64 `json:"completion_ratio"`
	RELIABILITY                          		float64 `json:"reliability"`
}

// Init is called during chaincode instantiation to initialize any
// data. Note that chaincode upgrade also calls this function to reset
// or to migrate data.
func (t *SimpleAsset) Init(stub shim.ChaincodeStubInterface) peer.Response {
	// Get the args from the transaction proposal
	args := stub.GetStringArgs()
	if len(args) != 3 {
		return shim.Error("Incorrect arguments. Expecting a key and a value")
	}
	ID := args[0]
	ra, err := strconv.ParseFloat(args[1], 64)
	if err != nil {
		return shim.Error("Completion_ratio input error")
	}
	re, err := strconv.ParseFloat(args[2], 64)
	if err != nil {
		return shim.Error("Reliability input error")
	}
	vehicle := &Vehicle{ID, ra, re}
	bsJSONasBytes, err := json.Marshal(vehicle)
	if err != nil {
		return shim.Error(err.Error())
	}
	// Set up any variables or assets here by calling stub.PutState()

	// We store the key and the value on the ledger
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

	// var result string
	// var results bytes.Buffer
	// var err error
	if fn == "set" {
		return t.set(stub, args)
	} else if fn == "del" {
		return t.del(stub, args)
	} else if fn == "mul_get" {
		return t.mul_get(stub, args)
	} else if fn == "mul_set"{
		return t.mul_set(stub, args)
	} else if fn=="bslist" {
		return t.QueryAllBSs(stub, args)
	} else if fn=="delall" {
		return t.delAllBSs(stub, args)
	} else { // assume 'get' even if fn is nil
		return t.get(stub, args)
	}
}

// Set stores the asset (both key and value) on the ledger. If the key exists,
// it will override the value with the new one
func (t *SimpleAsset) set(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	if len(args) != 3 {
		return shim.Error("Incorrect arguments. Expecting a key and a value")
	}
	ID := args[0]
	ra, err := strconv.ParseFloat(args[1], 64)
	if err != nil {
		return shim.Error("Completion ratio input error")
	}
	re, err := strconv.ParseFloat(args[2], 64)
	if err != nil {
		return shim.Error("Reliability input error")
	}
	vehicle := &Vehicle{ID, ra, re}
	bsJSONasBytes, err := json.Marshal(vehicle)
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(ID, bsJSONasBytes)

	if err != nil {
		return shim.Error(err.Error())
	}
	fmt.Println("Successful set state of vehicle" + args[0])
	return shim.Success(nil)
}

// Set or update a set of data.
func (t *SimpleAsset) mul_set(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	if (len(args)%3) != 0 {
		return shim.Error("Incorrect arguments. Expecting 3*n arguments")
	}
	var ID string
	var ra,re float64
	var err error
	var vehicle Vehicle
	var bsJSONasBytes []byte
	for i := 0; i < (len(args)/3); i++ {
		ID = args[3*i]
		ra, err = strconv.ParseFloat(args[3*i+1], 64)
		if err != nil {
			return shim.Error("Completion ratio input error")
		}
		re, err = strconv.ParseFloat(args[3*i+2], 64)
		if err != nil {
			return shim.Error("Reliability input error")
		}
		vehicle = Vehicle{ID, ra, re}
		bsJSONasBytes, err = json.Marshal(vehicle)
		if err != nil {
			return shim.Error(err.Error())
		}
		err = stub.PutState(ID, bsJSONasBytes)
		if err != nil {
			return shim.Error(err.Error())
		}
	}
	fmt.Println("Successful set state of vehicle" + args[0])
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
		jsonResp = "{\"Error\":\"Failed to delete the state of vehicle" + args[0] + "\"}"
		return shim.Error(jsonResp)
	}
	fmt.Println("Successful delete the state of vehicle" + args[0])
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
		jsonResp = "{\"Error\":\"Failed to get the state of vehicle: " + args[0] + "\"}"
		return shim.Error(jsonResp)
	}
	if value == nil {
		jsonResp = "{\"Error\":\"Vehicle does not exist " + args[0] + "\"}"
		return shim.Error(jsonResp)
	}
	return shim.Success(value)
}
func (t *SimpleAsset) QueryAllBSs(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	var jsonResp string
	var assets bytes.Buffer
	endKey := ""
	startKey := ""
	if len(args) != 0{
		startKey	= args[0]
		endKey		= args[1]
	}
	fmt.Printf(startKey)
	resultsIterator, err := stub.GetStateByRange(startKey, endKey)

	if err != nil {
		jsonResp = "{\"Error\":\"Failed to get the state of vehicle \"}"
		return shim.Error(jsonResp)
	}
	bAlreadyWritten := false
	defer resultsIterator.Close()
	assets.WriteString("[")
	for resultsIterator.HasNext(){
		aKeyValue, err := resultsIterator.Next()
		if err != nil {
			jsonResp = "{\"Error\":\"Failed to get the state of vehicle \"}"
			return shim.Error(jsonResp)
		}
		querykeyAsStr := aKeyValue.Key
		queryValAsBytes := aKeyValue.Value

		if bAlreadyWritten {
			assets.WriteString(",")
		}
		assets.WriteString("{\"id\":")
		assets.WriteString("\"")
		assets.WriteString(querykeyAsStr)
		assets.WriteString("\"")

		assets.WriteString(", \"Record\":")
		assets.Write(queryValAsBytes)
		assets.WriteString("}")
		bAlreadyWritten = true
	}
	assets.WriteString("]")
	return shim.Success(assets.Bytes())

}
func (t *SimpleAsset) delAllBSs(stub shim.ChaincodeStubInterface, args []string) peer.Response {
	var jsonResp string
	// var results bytes.Buffer
	var res_str []string
	endKey := ""
	startKey := ""
	if len(args) != 0{
		startKey	= args[0]
		endKey		= args[1]
	}
	resultsIterator, err := stub.GetStateByRange(startKey, endKey)

	if err != nil {
		jsonResp = "{\"Error\":\"Failed to get the state of vehicle \"}"
		return shim.Error(jsonResp)
	}
	// basestation := new(BaseStation)
	// results := []QueryResult{}
	// results := []byte{}"0","0","0","0"]}'
	// bAlreadyWritten := false
	defer resultsIterator.Close()
	for resultsIterator.HasNext(){
		queryResponse, err := resultsIterator.Next()

		if err != nil {
			jsonResp = "{\"Error\":\"Failed to get the state of vehicle \"}"
			return shim.Error(jsonResp)
		}

		queryResult := queryResponse.Key
		res_str = append(res_str, queryResult)
	}
	for i,s := range res_str {
		err := stub.DelState(s)
		if err != nil {
			jsonResp = "{\"Error\":\"Failed to delete the state of vehicle" + res_str[i]+ "\"}"
			return shim.Error(jsonResp)
		}
		// results.WriteString(res_str[i])
	}
	// return shim.Success(results.Bytes())
	return shim.Success(nil)
}
// Get returns the value of the specified asset key
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
