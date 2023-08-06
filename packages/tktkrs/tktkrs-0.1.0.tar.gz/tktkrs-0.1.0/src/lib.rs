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
        if self.data.len()<(page+1)*row_len{
             self.data.clone()[page*row_len..].to_vec()
        }else{
            self.data.clone()[page*row_len..(page+1)*row_len].to_vec()
        }
    }
}

#[pymodule]
fn tktkrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Database>()?;
    Ok(())
}
