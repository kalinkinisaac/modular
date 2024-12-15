# Modular
An algorithm for constructing fundamental domains and independent sets of generators for subgroups of the modular group.

## How to Launch
You can run the app using any of the following methods:

---

### 1. **Hosted Website**
Access the web application directly at:  
[https://kalinkinisaac.pythonanywhere.com](https://kalinkinisaac.pythonanywhere.com)

---

### 2. **Local Setup**

#### Clone the Repository
Start by cloning the project repository to your local machine. Open a terminal and run:

```bash
git clone https://github.com/kalinkinisaac/modular.git
cd modular
```

---

#### **Python Setup**

1. **Install Python 3.12**  
   Download and install Python 3.12 from the [official website](https://www.python.org/downloads/release/python-3120/).

2. **Set Up a Virtual Environment**  
   Create and activate a virtual environment to manage dependencies:

   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Dependencies**  
   Install the necessary packages by running:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**  

   - **Webserver Application**  
     Launch the web server using:

     ```bash
     python run_website.py
     ```

     Open a browser and navigate to:  
     [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

   - **Desktop Window Application**  
     Launch the desktop application using:

     ```bash
     python run_qt_window.py
     ```

     The desktop application window should appear.

---

#### **Docker Setup**

Using Docker simplifies deployment by bundling all dependencies into a container.

1. **Install Docker**  
   Download and install Docker from the [official website](https://docs.docker.com/get-started/get-docker/).

2. **Build the Docker Image**  
   From the project directory, build the Docker container:

   ```bash
   docker build . --tag modular
   ```

3. **Run the Docker Container**  
   Start the container with:

   ```bash
   docker run -d -p 8000:8000 modular
   ```

   This will output a container ID.
4. **Access the Application**  
   Open your browser and go to:  
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
5. **Stop the Docker Container**  
   After you have finished with the app you can stop the running container:

   ```bash
   docker stop <container-id>
   ```
