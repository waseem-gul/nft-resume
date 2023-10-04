// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts@4.9.3/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.9.3/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts@4.9.3/access/Ownable.sol";

contract NFTResume is ERC721, ERC721Burnable, Ownable {
    uint256 public tokenCount = 0;  // to keep track of total tokens minted
    string public baseTokenURI;

    constructor(string memory _baseTokenURI) ERC721("NFT Resume", "NFTR") {
        baseTokenURI = _baseTokenURI;  // set the base URI upon deployment
    }

    function _baseURI() internal view override returns (string memory) {
        return baseTokenURI;
    }

    // Allow users to mint their own tokens
    function mint(address to) external {
        tokenCount++;
        _safeMint(to, tokenCount);
    }

    // Allow changing the base URI in case your server changes
    function setBaseURI(string memory _baseTokenURI) external onlyOwner {
        baseTokenURI = _baseTokenURI;
    }
}
