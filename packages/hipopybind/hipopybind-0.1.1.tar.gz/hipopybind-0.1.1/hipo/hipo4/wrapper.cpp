#include <iostream>
#include "reader.h"
#include "event.h"
#include "writer.h"

hipo::reader      hipo_FORT_Reader;
hipo::event       hipo_FORT_Event;
hipo::dictionary  hipo_FORT_Dictionary;
hipo::writer      hipo_FORT_Writer;

std::map<std::string, hipo::bank *> eventStore;
std::string banklist;
std::string entrieslist;
std::string entriestypeslist;

extern "C" {

  void hipo_file_open_( const char *filename, int length){
    char *buffer = (char *) malloc(length+1);
    memcpy(buffer,filename,length);
    buffer[length] = '\0';
    printf("[FORTRAN] opening file : %s\n", buffer);
    hipo_FORT_Reader.open(buffer);
    hipo_FORT_Reader.readDictionary(hipo_FORT_Dictionary);
    free(buffer);
  }

  void hipo_file_open(const char *filename){
    hipo_FORT_Reader.open(filename);
    hipo_FORT_Reader.readDictionary(hipo_FORT_Dictionary);
  }

  int hipo_file_next_(int* fstatus){
    bool status = hipo_FORT_Reader.next();
    if(status==false){
      *fstatus = 12;
      return 12;
    }
    hipo_FORT_Reader.read(hipo_FORT_Event);
    std::map<std::string, hipo::bank *>::iterator it;
    for ( it = eventStore.begin(); it != eventStore.end(); it++ )
      {
         it->second->reset();   // string's value
      }
      *fstatus = 0;
      return 0;
  }

  /***** Write methods for banks (Gavalian/McEneaney) *****/

  //IMPORTANT: This step needs to happen before opening the file!
  void hipo_write_schema_(const char* schemaString, const char *name, int __group,int __item) {
    hipo::schema *schema = new hipo::schema(name, __group, __item);
    schema->parse(schemaString);

    hipo::dictionary *dict = new hipo::dictionary();
    dict->addSchema(*schema);
    hipo_FORT_Writer.addDictionary(*dict);
  }

  void hipo_add_schema_(const char* schemaString, const char *name, int __group,int __item) {
    hipo::schema *schema = new hipo::schema(name, __group, __item);
    schema->parse(schemaString);

    hipo::dictionary *dict = new hipo::dictionary();
    dict->addSchema(*schema);
    
    hipo_FORT_Writer.addDictionary(hipo_FORT_Dictionary);
    hipo_FORT_Writer.addDictionary(*dict);
  }

  void hipo_write_open_(const char* filename) {
    hipo_FORT_Writer.open(filename);
  }

  void hipo_write_flush_() { // Write current buffer
    hipo_FORT_Writer.flush();
  }

  void hipo_write_close_() {
    hipo_FORT_Writer.close();
  }

  void hipo_write_all_banks_() { //NOTE: This method obsolete.
    std::vector<std::string> schemaList = hipo_FORT_Dictionary.getSchemaList();
    for(int idx = 0; idx<schemaList.size(); idx++) {
      const char * buffer = schemaList[idx].c_str();
      hipo_FORT_Event.getStructure(*eventStore[buffer]); //IMPORTANT!  Have to getStructure before reading!
      hipo_FORT_Event.addStructure(*eventStore[buffer]); // IMPORTANT! Have to read event before you can do anything with it.
    } // for name in schemaList
  }

  void hipo_write_bank_(const char *name, const char** names, double** data, int bankCols, int bankRows, const char* dtype) {
    hipo::dictionary dict = hipo_FORT_Writer.getDictionary();
    hipo::schema schema = dict.getSchema(name);
    hipo::bank *bank = new hipo::bank(schema);
    bank->setRows(bankRows);

    const char* dtype_double = "D";
    const char* dtype_int    = "I";
    const char* dtype_float  = "F";
    
    for (int i=0; i<bankCols; i++){
      for (int j=0; j<bankRows; j++) {
        if (dtype==dtype_double)     bank->putDouble(names[i],j,data[i][j]);
        else if (dtype==dtype_int)   bank->putInt(names[i],j,(int)data[i][j]);
        else if (dtype==dtype_float) bank->putFloat(names[i],j,(float)data[i][j]);
        else bank->putDouble(names[i],j,data[i][j]);
      }
    }
    hipo_FORT_Event.addStructure(*bank); //NOTE: DO NOT do hipo_FORT_event.ggetStructure(*bank) HERE!!!
  }

  void hipo_add_event_() {
    hipo_FORT_Writer.addEvent(hipo_FORT_Event);
  }

  /***** END Write methods for banks *****/

  /***** Read methods for banks (Gavalian/McEneaney) *****/

  void hipo_read_all_banks_() {
    std::vector<std::string> schemaList = hipo_FORT_Dictionary.getSchemaList();
    for(int idx = 0; idx<schemaList.size(); idx++) {
      const char * buffer = schemaList[idx].c_str();
      if (eventStore.count(buffer)==0) {
          hipo::bank *bank_ptr = new hipo::bank(hipo_FORT_Dictionary.getSchema(buffer));
          eventStore[buffer]   = bank_ptr;
      }
      hipo_FORT_Event.getStructure(*eventStore[buffer]); // IMPORTANT! Have to read event before you can do anything with it.
    } // for name in schemaList
  }

  int hipo_go_to_event_(int* fstatus, int* eventNumber){
    bool status = hipo_FORT_Reader.gotoEvent(*eventNumber);
    if(status==false){
      *fstatus = 12;
      return 12;
    }
    hipo_FORT_Reader.read(hipo_FORT_Event);
    std::map<std::string, hipo::bank *>::iterator it;
    for ( it = eventStore.begin(); it != eventStore.end(); it++ )
      {
         it->second->reset();   // string's value
      }
      *fstatus = 0;
      return 0;
  }

  bool hipo_has_bank_(const char *bankname, int banknameLength) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';
    
    return hipo_FORT_Dictionary.hasSchema(buffer);
  }

  void hipo_show_banks_() {
    hipo_FORT_Dictionary.show();
  }

  void hipo_show_bank_(const char *bankname, int banknameLength) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    std::cout<<hipo_FORT_Dictionary.getSchema(buffer).getSchemaString()<<std::endl;
  }

  /**
  * Get greatest group # of all schema in hipo_FORT_Dictionary for appending banks.
  */
  int hipo_get_group_() {
    int group = 0;
    std::vector<std::string> schemaList = hipo_FORT_Dictionary.getSchemaList();
    for(int idx = 0; idx<schemaList.size(); idx++) {
      const char * buffer = schemaList[idx].c_str();
      int group_ = hipo_FORT_Dictionary.getSchema(buffer).getGroup();
      if (group_ > group) { group = group_; }
    }
    return group;
  }

  int hipo_get_bank_rows_(const char *bankname, int banknameLength) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    // Read event in and get # of bank rows
    hipo_FORT_Event.getStructure(*eventStore[buffer]);
    return eventStore[buffer]->getRows();
  }

  int hipo_get_bank_entries_(const char *bankname, int banknameLength) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    // Get bank entries
    return hipo_FORT_Dictionary.getSchema(buffer).getEntries();
  }

  //NOTE: This uses the `std::string banklist` variable defined at the top of the file.
  const unsigned char *hipo_get_banks_() {
    std::vector<std::string> schemaList = hipo_FORT_Dictionary.getSchemaList();
    std::string name;
    std::string separator = " ";
    for(int idx = 0; idx<schemaList.size(); idx++) {
      name = schemaList[idx];
      banklist = banklist + name;
      if (idx<schemaList.size()-1) { banklist = banklist + separator; }
    }
    const unsigned char *entries = reinterpret_cast<const unsigned char*>(banklist.c_str());

    return entries;
  }

  //NOTE: This uses the `std::string entrieslist` variable defined at the top of the file.
  const unsigned char *hipo_get_bank_entries_names_(const char *bankname, int banknameLength) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    hipo::schema schema = hipo_FORT_Dictionary.getSchema(buffer);
    int nEntries = schema.getEntries();
    std::string name;
    std::string separator = " ";
    for (int idx=0; idx<nEntries; idx++) {
      name = schema.getEntryName(idx);
      entrieslist = entrieslist + name;
      if (idx<nEntries-1) { entrieslist = entrieslist + separator; }
    }
    const unsigned char *entries = reinterpret_cast<const unsigned char*>(entrieslist.c_str());
    
    return entries;
  }

  //NOTE: This uses the `std::string entriestypeslist` variable defined at the top of the file.
  const unsigned char *hipo_get_bank_entries_names_types_(const char *bankname, int banknameLength) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    entriestypeslist = hipo_FORT_Dictionary.getSchema(buffer).getSchemaString();
    const unsigned char *entries = reinterpret_cast<const unsigned char*>(entriestypeslist.c_str());
    return entries;
  }

  /*
  *  Helper method for hipo_get_bank_entries_types_() below.
  *  NOTE: This is HARD-CODED to be the inverse of the 
  *  schema::getTypeByString() private method.
  */
  const char *getTypeByInt(int i) {
      if(i==1){
        return "B";
      } else if(i==2) {
        return "S";
      } else if(i==3) {
        return "I";
      } else if(i==4) {
        return "F";
      } else if(i==5) {
        return "D";
      } else if(i==8) {
        return "L";
      }
      return "U";
  }

  void hipo_get_bank_entries_types_(const char *bankname, int banknameLength, const char **entries) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    hipo::schema schema = hipo_FORT_Dictionary.getSchema(buffer);
    const int nEntries  = schema.getEntries();
    for (int i=0; i<nEntries; i++) {
      entries[i] = getTypeByInt(schema.getEntryType(i));
    }

  }

  void hipo_read_bank_(const char *bankname, int banknameLength, bool verbose) {
    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';
    if (eventStore.count(std::string(buffer))==0) {
      if (hipo_FORT_Dictionary.hasSchema(buffer)==true) {
        hipo::bank *bank_ptr = new hipo::bank(hipo_FORT_Dictionary.getSchema(buffer));
        eventStore[buffer]   = bank_ptr;
         
        if (verbose) {
          printf("---> map : initializing bank \"%24s\" (%6d, %5d) to the store\n",
          buffer,hipo_FORT_Dictionary.getSchema(buffer).getGroup(),
          hipo_FORT_Dictionary.getSchema(buffer).getItem() );
        }

      } else { free(buffer); return; }
    }
    hipo_FORT_Event.getStructure(*eventStore[buffer]); // IMPORTANT! Have to read event before you can do anything with it.
    if (verbose) eventStore[buffer]->show();
    free(buffer);
  }

  /***** END Read methods for banks *****/

  /***** Get methods for bank column arrays (McEneaney) *****/

  void hipo_get_ints(const char *bankname, int banknameLength, const char *item, int itemLength, int* data) {

    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    char *buffer_item = (char * ) malloc(itemLength+1);
    memcpy(buffer_item,item,itemLength);
    buffer_item[itemLength] = '\0';

    int bankRows = eventStore[buffer]->getRows();
    for (int i=0; i<bankRows; i++) { data[i] = eventStore[buffer]->getInt(buffer_item,i); }

  }

  void hipo_get_floats(const char *bankname, int banknameLength, const char *item, int itemLength, float* data) {

    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    char *buffer_item = (char * ) malloc(itemLength+1);
    memcpy(buffer_item,item,itemLength);
    buffer_item[itemLength] = '\0';

    int bankRows = eventStore[buffer]->getRows();
    for (int i=0; i<bankRows; i++) { data[i] = eventStore[buffer]->getFloat(buffer_item,i); }

  }

  void hipo_get_doubles(const char *bankname, int banknameLength, const char *item, int itemLength, double* data) {

    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    char *buffer_item = (char * ) malloc(itemLength+1);
    memcpy(buffer_item,item,itemLength);
    buffer_item[itemLength] = '\0';

    int bankRows = eventStore[buffer]->getRows();
    for (int i=0; i<bankRows; i++) { data[i] = eventStore[buffer]->getDouble(buffer_item,i); }

  }

  void hipo_get_shorts(const char *bankname, int banknameLength, const char *item, int itemLength, short* data) {

    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    char *buffer_item = (char * ) malloc(itemLength+1);
    memcpy(buffer_item,item,itemLength);
    buffer_item[itemLength] = '\0';

    int bankRows = eventStore[buffer]->getRows();
    for (int i=0; i<bankRows; i++) { data[i] = eventStore[buffer]->getShort(buffer_item,i); }

  }

  void hipo_get_longs(const char *bankname, int banknameLength, const char *item, int itemLength, long* data) {

    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    char *buffer_item = (char * ) malloc(itemLength+1);
    memcpy(buffer_item,item,itemLength);
    buffer_item[itemLength] = '\0';

    int bankRows = eventStore[buffer]->getRows();
    for (int i=0; i<bankRows; i++) { data[i] = eventStore[buffer]->getLong(buffer_item,i); }

  }

  void hipo_get_bytes(const char *bankname, int banknameLength, const char *item, int itemLength, long* data) {

    char *buffer = (char * ) malloc(banknameLength+1);
    memcpy(buffer,bankname,banknameLength);
    buffer[banknameLength] = '\0';

    char *buffer_item = (char * ) malloc(itemLength+1);
    memcpy(buffer_item,item,itemLength);
    buffer_item[itemLength] = '\0';

    int bankRows = eventStore[buffer]->getRows();
    for (int i=0; i<bankRows; i++) { data[i] = eventStore[buffer]->getByte(buffer_item,i); }

  }

  /***** END get methods for bank column arrays *****/

} // END extern "C"
