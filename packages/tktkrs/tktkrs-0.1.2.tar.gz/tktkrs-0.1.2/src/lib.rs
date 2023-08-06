use pyo3::prelude::*;

#[pyclass]
struct Database{
    data:Vec<Vec<Vec<String>>>,
}

#[pymethods]
impl Database {
    #[new]
    fn new()->Self{
        Database { data: Vec::new() }
    }
    
    fn insert_data(&mut self,data_in:Vec<Vec<String>>){
        self.data.push(data_in);
    }
    fn get_all(&self)->Vec<Vec<Vec<String>>>{
        self.data.clone()
    }
    fn get_len(&self)->usize{
        self.data.len()
    }
    fn clear_data(&mut self){
        self.data.clear()
    }
    fn get_show_data(&self,page:usize,row_len:usize)->Vec<Vec<Vec<String>>>{
        if (page+1)*row_len>=self.data.len(){
            self.data.clone()[page*row_len..].to_vec()

        }else{
            self.data.clone()[page*row_len..(page+1)*row_len].to_vec()
        }
    }
}

#[pyfunction]
fn gif_info(path:String) -> Vec<u16> {
    use std::fs::File;
    let mut timedelay:Vec<u16> = Vec::new();
    if let Ok(input) = File::open(path)
    {
        let options = gif::DecodeOptions::new();
        if let Ok(mut decoder) = options.read_info(input){
            while let Some(frame) = decoder.read_next_frame().unwrap() {
                    timedelay.push(frame.delay*10);
                    // println!("{}",frame.delay);
            }  

        }
    
    }
    timedelay
}

#[pymodule]
fn tktkrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Database>()?;
    m.add_function(wrap_pyfunction!(gif_info, m)?)?;
    Ok(())
}
