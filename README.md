---
typora-root-url: ./back-end\data
---

# 1. 简易的二维码图片检测效果如下：

最终效果：

![](/last_view/屏幕截图(16).png)

![](/last_view/屏幕截图(17).png)

![](/last_view/屏幕截图(18).png)

![](/last_view/屏幕截图(19).png)

![](/last_view/屏幕截图(20).png)

# 2. CNN模型：

运行这段代码时，首先会定义一个`ConvNet`类，该类继承自`nn.Module`。在`ConvNet`类的构造函数中，定义了一系列卷积层和池化层，以及全连接层，来构建卷积神经网络模型。

在前向传播过程中，将输入数据传递给卷积层，然后通过激活函数和池化层进行特征提取和降维。接下来，将得到的特征展平，并通过全连接层进行分类。最后，将输出的结果返回。

在训练过程中，使用数据集和数据加载器来获取训练样本。对于每个批次的数据，将输入数据传递给模型进行前向传播，并计算损失值。然后，通过反向传播和优化器更新模型的参数。在每个训练周期结束后，计算损失和准确率，并根据最佳准确率保存模型参数。



这里的话我就用训练好的 best_model.pkl 模型。

# 3. CNN模型预测：

预测接口：

模型的预测接口通过调用`forward`方法来实现。在训练过程中，预测是通过调用`net(inputs)`来完成的。

具体来说，输入的图像数据`inputs`通过使用`Variable`函数进行封装，以便进行自动求导。然后，封装后的输入数据被传递给模型的`forward`方法，即`output = net(inputs)`。

在`forward`方法中，输入数据经过卷积层和池化层进行特征提取和降维处理，然后通过展平操作和全连接层进行分类。最终，模型的输出结果`output`表示每个样本的预测结果。

在训练过程中，使用预测结果计算损失，并通过反向传播和优化器来更新模型的参数。在测试或预测阶段，可以直接使用`output`来获取模型的预测结果。

总结起来，模型的预测接口是通过调用`forward`方法并传递输入数据来获得模型的输出结果。



# 4. Flask 部署：

然后通过Flask框架写相应函数：

```python
@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    t = str(file)
    pattern = r"'([^']*)'"
    match = re.findall(pattern, t)
    if match:
        first_char = match[0]
    else:
        print("未找到匹配项")
        
    img_path = 'back-end/data/image/' + first_char
    predicted_number = predict_number(img_path)
    print('Predicted number:', predicted_number)
    return jsonify({'predicted_number': predicted_number.tolist()})

```

这样前端发出POST请求时，会对上传的图像进行处理。

# 5. VUE前端：

主要是通过VUE编写前端WEB框架。

核心前后端交互代码：

```java
<script>
import axios from "axios";

export default {
  data() {
    return {
      imageUrl: null,
      predictedNumber: null
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.imageUrl = reader.result;
        const formData = new FormData();
        formData.append("image", file);
        axios.post("http://127.0.0.1:5000/api/upload", formData).then(response => {
          console.log(response.data);
          this.predictedNumber = response.data.predicted_number.join("");
        });
      };
    },

    
    
  }
};
</script>
```



# 6. 启动项目：

cd到后端项目文件夹back-end，安装requirement.txt文档下的依赖

```bash
pip install -r requirements.txt
```

然后在 Flask 后端项目下启动后端代码：

```bash
python app.py
```



cd到在 VUE 前端项目下front-end，先安装依赖：

```bash
npm install
```

然后运行前端：

```bash
npm run serve
```

然后在浏览器打开localhost即可：


