torch.nn.Module.register_forward_hook(hook_function)

(1) torch document, (2) 한글 설명 tutorial

Network의 특정 module에서의 input, ouput을 확인하고 싶거나, 바꾸고 싶을 때 사용한다.

해당 nn.moulde의 forward가 실행된 직후에 설정해 놓은 함수*가 실행된다. 어떻게든 register_forward_hook를 정의해 놓는 순간부터, 해당 코드에서 Network 전체 forward가 돌아가면 무조건 그 함수*가 실행된다.

아래와 같이 global을 사용하지 않더라고 전역변수처럼 변수를 모듈 내부에서 사용할 수 있다.

```
# use lists to store the outputs via up-values
conv_features, enc_attn_weights, dec_attn_weights = [], [], []
      
hooks = [
    model.backbone[-2].register_forward_hook(
        lambda self, input, output: conv_features.append(output)
    ),
    model.transformer.encoder.layers[-1].self_attn.register_forward_hook(
        lambda self, input, output: enc_attn_weights.append(output[1])
    ),
    model.transformer.decoder.layers[-1].multihead_attn.register_forward_hook(
        lambda self, input, output: dec_attn_weights.append(output[1])
    ),
]
      
# propagate through the model
outputs = model(img)
      
for hook in hooks:
    hook.remove()
    # forward 이후에 실행해달라고 만들어 놓은 함수가 hook이다. 
    # 이 hook을 제거한다. (network를 원상복구한다.)
      
# don't need the list anymore
conv_features = conv_features[0] # 최종 feature map의 width, hight를 파악하기 위해서. 
enc_attn_weights = enc_attn_weights[0] # 마지막 encoder layer의 attention score를 파악하기 위해서.
dec_attn_weights = dec_attn_weights[0] # 마지막 decoder layer의 attention score를 파악하기 위해서.
```
