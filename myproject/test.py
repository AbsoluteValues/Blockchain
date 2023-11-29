import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain :
    def __init__(self) :
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')


    def create_block(self, proof, previous_hash) : # 블록체인에서 Block에 들어가는 기본적인 데이터 만들어주는 함수
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash
        }

        self.chain.append(block)
        return block
    

    def get_previous_block(self) : # 이전 Block을 받아오는 함수
        return self.chain[-1]
    

    def proof_of_work(self, previous_proof) : # 일을 증명하는 함수
        new_proof = 1
        check_proof = False

        while check_proof is False : # 올바른 증명인지 확인
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest() # Block 암호화
            
            if hash_operation.startswith('0000') : # 올바른 증명의 확인 조건
                check_proof = True
            else :
                new_proof += 1

        return new_proof
    

    # Python 객체를 Json 문자열로 전환하여 암호화하는 함수
    def hash(self, block) :
        encoded_block = json.dumps(block, sort_keys = True).encode() 
        return hashlib.sha256(encoded_block).hexdigest()
    

    # 유효한 Chain인지 확인하는 함수
    def is_valid_chain(self, chain) :
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain) : # Block의 Index보다 Chain의 길이가 더 클 때 까지
            block = chain[block_index] 

            if block['previous_hash'] != self.hash(previous_block) : # 이전 Block을 Hash로 변환한 것이 Block의 이전 Hash와 일치 하지 않으면 반환
                return False
            
            previous_proof = previous_block['proof'] # 이전 Block의 증명 받기
            proof = block['proof'] # Block의 증명 받기
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest() # Block 암호화

            if not hash_operation.startswith('0000') : # 올바른 증명의 확인 조건
                return False
            
            previous_block = block
            block_index += 1

        return True


# Flask 초기 설정
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain = Blockchain()


# 채굴하는 페이지의 함수
@app.route('/mine_block', methods = ['GET'])
def mine_block() :
    previous_block = blockchain.get_previous_block() # 이전 Block 받기
    previous_proof = previous_block['proof'] # 이전 Block의 증명 받기
    proof = blockchain.proof_of_work(previous_proof) # 이전 증명에 대한 일을 증명
    previous_hash = blockchain.hash(previous_block) # 이전 Block의 Hash 받기
    block = blockchain.create_block(proof, previous_hash) # 새로운 Block을 생성

    response = {
        'message' : 'Congratulations, you just mined a block!', **block
    }

    return jsonify(response), 200


# 만들어진 Block을 확인하는 함수
@app.route('/get_chain', methods = ['GET'])
def get_chain() :
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200



# 실행
app.run(host = '127.0.0.1', port = 5000)
