### This is belong to final year project of my study program at HUST
### GAN-MF (Generative Adversarial Network for Matrix Factorization)
GAN-MF is an implementation of a Generative Adversarial Network (GAN) for Matrix Factorization. It is a novel approach to collaborative filtering that leverages the power of GANs to learn informative representations of user-item interactions for recommendation.

### How GAN-MF Works
GAN-MF consists of two main components: the generator and the discriminator. The generator takes as input user embeddings and generates item embeddings, while the discriminator tries to distinguish between real item embeddings from the training data and fake item embeddings generated by the generator. The generator and discriminator are trained adversarially, where the generator tries to fool the discriminator, and the discriminator tries to correctly classify real and fake item embeddings.

## Requirements:
    matplotlib==3.0.2
    numpy==1.16.2
    pandas==0.24.1
    seaborn==0.9.0
    tensorflow==2.12.0
    tqdm==4.31.1
### Usage
  Clone this repository.
  Install the required dependencies using pip install -r requirements.txt.
  Prepare your user-item interaction data in a matrix format, where rows represent users and columns represent items. You can preprocess the data and convert it to a dense or sparse matrix format depending on the size of your dataset.
  Modify the hyperparameters in the config.py file according to your dataset and preferences. You can adjust the learning rate, number of epochs, batch size, number of hidden layers, and more.
  Run the train.py script to start training the GAN-MF model on your dataset.

## References
Original GAN Paper
Collaborative Filtering with Generative Adversarial Networks
Contributing
If you find any bugs or have suggestions for improvement, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
