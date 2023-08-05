#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>

#include <hipo/hipo4/utils.h>
#include <hipo/hipo4/datastream.h>
#include <hipo/hipo4/dictionary.h>
#include <hipo/hipo4/bank.h>
#include <hipo/hipo4/event.h>
#include <hipo/hipo4/reader.h>
#include <hipo/hipo4/record.h>
#include <hipo/hipo4/recordbuilder.h>
#include <hipo/hipo4/writer.h>
#include <hipo/hipo4/hipoexceptions.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

//NOTE: Shared object will not load if you simultaneously 
// define classes to bind within this file and bind hipo 
// classes or classes from another cpp project.

//--------------------------------------------------//
// HIPO Trampoline classes

//NOTE: utils, benchmark classes throw compilation error if you try to use trampoline class.

template <class DatastreamBase = hipo::datastream> class PyDatastream : public DatastreamBase {
public:
    using DatastreamBase::DatastreamBase; // Inherit constructors
    long size() override { PYBIND11_OVERRIDE_PURE(long, DatastreamBase, size, ); }
    long position() override { PYBIND11_OVERRIDE_PURE(long, DatastreamBase, position, ); }
    long position(long pos) override { PYBIND11_OVERRIDE_PURE(long, DatastreamBase, position, pos); }
    void open(const char *filename) override { PYBIND11_OVERRIDE_PURE(void, DatastreamBase, open, filename ); }
    int read(char *s, int size) override { PYBIND11_OVERRIDE_PURE(int, DatastreamBase, read, s, size); }
};

//NOTE: datastreamLocalFile, datastreamXrootd classes thorw compilation error if you try to use trampoline class.

template <class SchemaBase = hipo::schema> class PySchema : public SchemaBase {
public:
    using SchemaBase::SchemaBase; // Inherit constructors
};

template <class DictionaryBase = hipo::dictionary> class PyDictionary : public DictionaryBase {
public:
    using DictionaryBase::DictionaryBase; // Inherit constructors
};

template <class StructureBase = hipo::structure> class PyStructure : public StructureBase {
public:
    using StructureBase::StructureBase; // Inherit constructors
    void notify() override { PYBIND11_OVERRIDE_PURE(void, StructureBase, notify, ); }
};

template <class BankBase = hipo::bank> class PyBank : public PyStructure<BankBase> {
public:
    using PyStructure<BankBase>::PyStructure; // Inherit constructors
};

template <class EventBase = hipo::event> class PyEvent : public EventBase {
public:
    using EventBase::EventBase; // Inherit constructors
};

//NOTE: readerIndex, reader, data, record classes throw compilation error if you try to use trampoline class.

template <class RecordBuilderBase = hipo::recordbuilder> class PyRecordBuilder : public RecordBuilderBase {
public:
    using RecordBuilderBase::RecordBuilderBase; // Inherit constructors
};

template <class WriterBase = hipo::writer> class PyWriter : public WriterBase {
public:
    using WriterBase::WriterBase; // Inherit constructors
};

//--------------------------------------------------//
// Python Module Bindings

namespace py = pybind11;
PYBIND11_MODULE(hipopybind, m) {

    //----------------------------------------------------------------------//
    // Bind HIPO utils
    py::class_<hipo::utils> utils(m, "Utils");
    utils.def(py::init<>());

    utils.def("tokenize", &hipo::utils::tokenize);
    utils.def("substring", &hipo::utils::substring);
    utils.def("findposition", &hipo::utils::findposition);
    utils.def("ltrim", &hipo::utils::ltrim);
    utils.def("rtrim", &hipo::utils::rtrim);
    utils.def("trim", &hipo::utils::trim);

    utils.def("printLogo", &hipo::utils::printLogo);

    utils.def("getHeader", &hipo::utils::getHeader);
    utils.def("getFileHeader", &hipo::utils::getFileHeader);
    utils.def("getFileTrailer", &hipo::utils::getFileTrailer);
    utils.def("getSConstruct", &hipo::utils::getSConstruct);

    utils.def("writeInt", &hipo::utils::writeInt);
    utils.def("writeLong", &hipo::utils::writeLong);
    utils.def("writeByte", &hipo::utils::writeByte);

    //----------------------------------------------------------------------//
    // Bind HIPO benchmark
    py::class_<hipo::benchmark> benchmark(m, "Benchmark");
    benchmark.def(py::init<>());
    benchmark.def(py::init([](const char *name) { return new hipo::benchmark(name); }));
    benchmark.def(py::init([](int freq) { return new hipo::benchmark(freq); }));

    benchmark.def("setName", &hipo::benchmark::setName);
    benchmark.def("resume", &hipo::benchmark::resume);
    benchmark.def("pause", &hipo::benchmark::pause);
    benchmark.def("getTime", &hipo::benchmark::getTime);
    benchmark.def("getTimeSec", &hipo::benchmark::getTimeSec);
    benchmark.def("getCounter", &hipo::benchmark::getCounter);
    benchmark.def("show", &hipo::benchmark::show);

//   class benchmark {
//      private:

//        std::chrono::high_resolution_clock clock;
//        std::chrono::time_point<std::chrono::high_resolution_clock> first, second;
//        std::string  benchmarkName;

//        long running_time;
//        int  counter;
//        int  printoutFrequency;

    // //----------------------------------------------------------------------// //NOTE: Ran into flat namespace error again when loading this in python after compilation
    // // Bind HIPO datastream
    // py::class_<hipo::datastream, PyDatastream<>> datastream(m, "Datastream");
    // datastream.def(py::init<>());

    // datastream.def("size", &hipo::datastream::size); //TODO: These are virtual methods... need to override above...
    // datastream.def("position", static_cast<long (hipo::datastream::*)()>(&hipo::datastream::position), "position");
    // datastream.def("position", static_cast<long (hipo::datastream::*)(long)>(&hipo::datastream::position), "position");
    // datastream.def("open", &hipo::datastream::open);
    // datastream.def("read", &hipo::datastream::read);

// class datastream {
//     private:
//        std::ifstream     inputStream;
//        std::string       remoteAddress;
//        int               streamType = 1;

    // //----------------------------------------------------------------------// //NOTE: Ran into flat namespace error again when loading this in python after compilation
    // // Bind HIPO datastreamLocalFile
    // py::class_<hipo::datastreamLocalFile> datastreamLocalFile(m, "DatastreamLocalFile");
    // datastreamLocalFile.def(py::init<>());

    // datastreamLocalFile.def("size", &hipo::datastreamLocalFile::size); //TODO: These are virtual methods... need to override above...
    // datastreamLocalFile.def("position", static_cast<long (hipo::datastreamLocalFile::*)()>(&hipo::datastreamLocalFile::position), "position");
    // datastreamLocalFile.def("position", static_cast<long (hipo::datastreamLocalFile::*)(long)>(&hipo::datastreamLocalFile::position), "position");
    // datastreamLocalFile.def("open", &hipo::datastreamLocalFile::open);
    // datastreamLocalFile.def("read", &hipo::datastreamLocalFile::read);

// class datastreamLocalFile {

//   private:
//     std::ifstream     inputStream;

    // //----------------------------------------------------------------------// //NOTE: Ran into flat namespace error again when loading this in python after compilation
    // // Bind HIPO datastreamXrootd
    // py::class_<hipo::datastreamXrootd> datastreamXrootd(m, "DatastreamXrootd");
    // datastreamXrootd.def(py::init<>());

    // datastreamXrootd.def("size", &hipo::datastreamXrootd::size); //TODO: These are virtual methods... need to override above...
    // datastreamXrootd.def("position", static_cast<long (hipo::datastreamXrootd::*)()>(&hipo::datastreamXrootd::position), "position");
    // datastreamXrootd.def("position", static_cast<long (hipo::datastreamXrootd::*)(long)>(&hipo::datastreamXrootd::position), "position");
    // datastreamXrootd.def("open", &hipo::datastreamXrootd::open);
    // datastreamXrootd.def("read", &hipo::datastreamXrootd::read);

// class datastreamXrootd {
// private:
//   #ifdef __XrootD__
//           kXR_unt16 open_mode = (kXR_ur);
//           kXR_unt16 open_opts = (1);
//           XrdClient *cli = NULL;
//   #endif
//   long streamPosition = 0;

    //----------------------------------------------------------------------//
    // Bind HIPO schema
    py::class_<hipo::schema, PySchema<>> schema(m, "Schema");
    schema.def(py::init<>());
    schema.def(py::init([](const char *name, int __groupid, int __itemid) { return new hipo::schema(name, __groupid, __itemid); }));
    schema.def(py::init([](const hipo::schema &s) { return new hipo::schema(s); }));

    schema.def("parse", &hipo::schema::parse);
    schema.def("getName", &hipo::schema::getName);
    schema.def("getGroup", &hipo::schema::getGroup);
    schema.def("getItem", &hipo::schema::getItem);
    schema.def("getSizeForRows", &hipo::schema::getSizeForRows);
    schema.def("getRowLength", &hipo::schema::getRowLength);
    schema.def("getEntryOrder", &hipo::schema::getEntryOrder);
    schema.def("exists", &hipo::schema::exists);
    schema.def("getOffset", py::detail::overload_cast_impl<int, int, int>()(&hipo::schema::getOffset, py::const_), "getOffset"); //NOTE:  Need this syntax for const functions!
    schema.def("getOffset", py::detail::overload_cast_impl<const char*, int, int>()(&hipo::schema::getOffset, py::const_), "getOffset"); //NOTE:  Need this syntax for const functions!
    schema.def("getEntryType", &hipo::schema::getEntryType);
    schema.def("getEntryName", &hipo::schema::getEntryName);
    schema.def("getSchemaString", &hipo::schema::getSchemaString);
    schema.def("getSchemaStringJson", &hipo::schema::getSchemaStringJson);

    schema.def_property_readonly("schemaEntriesMap", nullptr);
    schema.def_property_readonly("schemaEntries", nullptr);
    schema.def_property_readonly("groupid", &hipo::schema::getGroup);
    schema.def_property_readonly("itemid", &hipo::schema::getItem);
    schema.def_property_readonly("rowLength", &hipo::schema::getRowLength);
    schema.def_property_readonly("warningCount", nullptr);
    schema.def_property_readonly("schemaName", &hipo::schema::getName);

    schema.def("__repr__", //TODO: Test this function in python
             [](hipo::schema &s) { std::string r("Schema : name = "+s.getName()+" , schemaString = "+s.getSchemaString()+"\n"); return r; }
    );
    schema.def("__eq__", //TODO: Test this function in python
        [](hipo::schema *s1, hipo::schema *s2) { return s1 == s2; }
    );
     schema.def("__len__", //TODO: Test this function in python
        [](hipo::schema &s) { return s.getRowLength(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO dictionary
    py::class_<hipo::dictionary, PyDictionary<>> dictionary(m, "Dictionary");
    dictionary.def(py::init<>());

    dictionary.def("getSchemaList", &hipo::dictionary::getSchemaList);
    dictionary.def("addSchema", &hipo::dictionary::addSchema);
    dictionary.def("hasSchema", &hipo::dictionary::hasSchema);
    dictionary.def("getSchema", &hipo::dictionary::getSchema);
    dictionary.def("parse", &hipo::dictionary::parse);
    dictionary.def("show", &hipo::dictionary::show);

    // schema.def_property_readonly("factory", nullptr);

    dictionary.def("__repr__", //TODO: Test this function in python
             [](hipo::dictionary &d) {
                std::vector<std::string> schemaList = d.getSchemaList();
                std::string r("Dictionary :\n");
                for(int idx = 0; idx<schemaList.size(); idx++) {
                    const char * buffer = schemaList[idx].c_str();
                    hipo::schema s = d.getSchema(buffer);
                    r += "\tSchema : name = "+s.getName()+" , schemaString = "+s.getSchemaString()+"\n";
                }
                return r;
                }
    );
    dictionary.def("__eq__", //TODO: Test this function in python
        [](hipo::dictionary *d1, hipo::dictionary *d2) { return d1 == d2; }
    );
    dictionary.def("__len__", //TODO: Test this function in python
        [](hipo::dictionary &d) { return d.getSchemaList().size(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO structure
    py::class_<hipo::structure, PyStructure<>> structure(m, "Structure");
    structure.def(py::init<>());
    structure.def(py::init([](int size) { return new hipo::structure(size); }));
    structure.def(py::init([](int __group, int __item, std::string &str) { return new hipo::structure(__group, __item, str); }));

    structure.def("allocate", &hipo::structure::allocate);
    structure.def("getSize", &hipo::structure::getSize);
    structure.def("getType", &hipo::structure::getType);
    structure.def("getGroup", &hipo::structure::getGroup);
    structure.def("getItem", &hipo::structure::getItem);
    structure.def("init", &hipo::structure::init);
    structure.def("initNoCopy", &hipo::structure::initNoCopy);
    structure.def("getAddress", &hipo::structure::getAddress);
    structure.def("show", &hipo::structure::show);
    structure.def("setSize", &hipo::structure::setSize);
    structure.def("getIntAt", &hipo::structure::getIntAt);
    structure.def("getShortAt", &hipo::structure::getShortAt);
    structure.def("getByteAt", &hipo::structure::getByteAt);
    structure.def("getFloatAt", &hipo::structure::getFloatAt);
    structure.def("getDoubleAt", &hipo::structure::getDoubleAt);
    structure.def("getLongAt", &hipo::structure::getLongAt);
    structure.def("getStringAt", &hipo::structure::getStringAt);
    structure.def("putIntAt", &hipo::structure::putIntAt);
    structure.def("putShortAt", &hipo::structure::putShortAt);
    structure.def("putByteAt", &hipo::structure::putByteAt);
    structure.def("putFloatAt", &hipo::structure::putFloatAt);
    structure.def("putDoubleAt", &hipo::structure::putDoubleAt);
    structure.def("putLongAt", &hipo::structure::putLongAt);
    structure.def("putStringAt", &hipo::structure::putStringAt);
    structure.def("notify", &hipo::structure::notify);

    structure.def("__repr__", //TODO: Test this function in python
             [](hipo::structure &s) { 
                std::string r("Structure : group = "); r += std::to_string(s.getGroup())+" , item = "+std::to_string(s.getItem())+" , type = "+std::to_string(s.getType())+" , length = "+std::to_string(s.getSize())+"\n";
                return r;
            }
    );
    structure.def("__eq__", //TODO: Test this function in python
        [](hipo::structure *s1, hipo::structure *s2) { return s1 == s2; }
    );
    structure.def("__len__", //TODO: Test this function in python
        [](hipo::structure &s) { return s.getSize(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO bank
    py::class_<hipo::bank, hipo::structure, PyBank<>> bank(m, "Bank");
    bank.def(py::init<>());
    bank.def(py::init([](const hipo::schema& __schema) { return new hipo::bank(__schema); }));
    bank.def(py::init([](const hipo::schema& __schema, int __rows) { return new hipo::bank(__schema, __rows); }));

    bank.def("getSchema", &hipo::bank::getSchema);
    bank.def("getRows", &hipo::bank::getRows);
    bank.def("setRows", &hipo::bank::setRows);

    bank.def("getInt", py::detail::overload_cast_impl<int, int>()(&hipo::bank::getInt, py::const_), "getInt");
    bank.def("getInt", py::detail::overload_cast_impl<const char*, int>()(&hipo::bank::getInt, py::const_), "getInt");
    bank.def("getShort", py::detail::overload_cast_impl<int, int>()(&hipo::bank::getShort, py::const_), "getShort");
    bank.def("getShort", py::detail::overload_cast_impl<const char*, int>()(&hipo::bank::getShort, py::const_), "getShort");
    bank.def("getByte", py::detail::overload_cast_impl<int, int>()(&hipo::bank::getByte, py::const_), "getByte");
    bank.def("getByte", py::detail::overload_cast_impl<const char*, int>()(&hipo::bank::getByte, py::const_), "getByte");
    bank.def("getFloat", py::detail::overload_cast_impl<int, int>()(&hipo::bank::getFloat, py::const_), "getFloat");
    bank.def("getFloat", py::detail::overload_cast_impl<const char*, int>()(&hipo::bank::getFloat, py::const_), "getFloat");
    bank.def("getDouble", py::detail::overload_cast_impl<int, int>()(&hipo::bank::getDouble, py::const_), "getDouble");
    bank.def("getDouble", py::detail::overload_cast_impl<const char*, int>()(&hipo::bank::getDouble, py::const_), "getDouble");
    bank.def("getLong", py::detail::overload_cast_impl<int, int>()(&hipo::bank::getLong, py::const_), "getLong");
    bank.def("getLong", py::detail::overload_cast_impl<const char*, int>()(&hipo::bank::getLong, py::const_), "getLong");

    bank.def("getInts", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getInts, py::const_), "getInts");
    bank.def("getShorts", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getShorts, py::const_), "getShorts");
    bank.def("getBytes", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getBytes, py::const_), "getBytes");
    bank.def("getFloats", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getFloats, py::const_), "getFloats");
    bank.def("getDoubles", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getDoubles, py::const_), "getDoubles");
    bank.def("getLongs", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getLongs, py::const_), "getLongs");

    bank.def("getDoubles", py::detail::overload_cast_impl<const char*>()(&hipo::bank::getDoubles, py::const_), "getDoubles");
    
    bank.def("putInt", py::detail::overload_cast_impl<int, int, int32_t>()(&hipo::bank::putInt), "putInt");
    bank.def("putInt", py::detail::overload_cast_impl<const char*, int, int32_t>()(&hipo::bank::putInt), "putInt");
    bank.def("putShort", py::detail::overload_cast_impl<int, int, int16_t>()(&hipo::bank::putShort), "putShort");
    bank.def("putShort", py::detail::overload_cast_impl<const char*, int, int16_t>()(&hipo::bank::putShort), "putShort");
    bank.def("putByte", py::detail::overload_cast_impl<int, int, int8_t>()(&hipo::bank::putByte), "putByte");
    bank.def("putByte", py::detail::overload_cast_impl<const char*, int, int8_t>()(&hipo::bank::putByte), "putByte");
    bank.def("putFloat", py::detail::overload_cast_impl<int, int, float>()(&hipo::bank::putFloat), "putFloat");
    bank.def("putFloat", py::detail::overload_cast_impl<const char*, int, float>()(&hipo::bank::putFloat), "putFloat");
    bank.def("putDouble", py::detail::overload_cast_impl<int, int, double>()(&hipo::bank::putDouble), "putDouble");
    bank.def("putDouble", py::detail::overload_cast_impl<const char*, int, double>()(&hipo::bank::putDouble), "putDouble");
    bank.def("putLong", py::detail::overload_cast_impl<int, int, int64_t>()(&hipo::bank::putLong), "putLong");
    bank.def("putLong", py::detail::overload_cast_impl<const char*, int, int64_t>()(&hipo::bank::putLong), "putLong");

    bank.def("putInts", py::detail::overload_cast_impl<const char*, std::vector<int32_t>>()(&hipo::bank::putInts), "putInts");
    bank.def("putShorts", py::detail::overload_cast_impl<const char*, std::vector<int16_t>>()(&hipo::bank::putShorts), "putShorts");
    bank.def("putBytes", py::detail::overload_cast_impl<const char*, std::vector<int8_t>>()(&hipo::bank::putBytes), "putBytes");
    bank.def("putFloats", py::detail::overload_cast_impl<const char*, std::vector<float>>()(&hipo::bank::putFloats), "putFloats");
    bank.def("putDoubles", py::detail::overload_cast_impl<const char*, std::vector<double>>()(&hipo::bank::putDoubles), "putDoubles");
    bank.def("putLongs", py::detail::overload_cast_impl<const char*, std::vector<int64_t>>()(&hipo::bank::putLongs), "putLongs");

    bank.def("show", &hipo::bank::show);
    bank.def("reset", &hipo::bank::reset);
    bank.def("notify", &hipo::bank::notify);

    bank.def_property_readonly("bankSchema", &hipo::bank::getSchema); //NOTE: Not really necessary.
    bank.def_property_readonly("bankRows", &hipo::bank::getRows);

    bank.def("__repr__", //TODO: Test this function in python
             [](hipo::bank &b) { 
                std::string r("Bank : name = "); r += b.getSchema().getName()+" , rows = "+std::to_string(b.getRows())+"\n";
                for (int i = 0; i < b.getSchema().getEntries(); i++) {
                    std::string x("\t"); x += b.getSchema().getEntryName(i)+" : "; r += x;
                    for (int k = 0; k < b.getRows(); k++) {
                        if (b.getSchema().getEntryType(i) < 4) {
                            r += std::to_string(b.getInt(i,k))+" "; // std::string y("%8d ", b.getInt(i,k)); r += y; // %8d
                        } else {
                            if (b.getSchema().getEntryType(i)==4) {
                                r += std::to_string(b.getFloat(i,k))+" "; // std::string y("%8.5f ",b.getFloat(i,k)); r += y; // %8.5f
                            }
                            if (b.getSchema().getEntryType(i)==5) {
                                r += std::to_string(b.getDouble(i,k))+" "; // std::string y("%8.5f ",b.getDouble(i,k)); r += y; // %8.5f
                            }
                            if (b.getSchema().getEntryType(i)==8) {
                                r += std::to_string(b.getLong(i,k))+" "; // std::string y("%14ld ", b.getLong(i,k)); r += y; // %14ld
                            }
                        } // else
                    } // for(int k = 0; k < b.getRows(); k++)
                    r += "\n";
                } // for(int i = 0; i < b.getSchema().getEntries(); i++)
                return r;
            } // [](hipo::bank &b)
    );
    bank.def("__eq__", //TODO: Test this function in python
        [](hipo::bank *b1, hipo::bank *b2) { return b1 == b2; }
    );
    bank.def("__len__", //TODO: Test this function in python
        [](hipo::bank &b) { return b.getRows(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO event
    py::class_<hipo::event, PyEvent<>> event(m, "Event");
    event.def(py::init<>());
    event.def(py::init([](int size) { return new hipo::event(size); }));

    event.def("show", &hipo::event::show);
    event.def("init", static_cast<void (hipo::event::*)(std::vector<char>&)>(&hipo::event::init), "init");
    event.def("init", static_cast<void (hipo::event::*)(const char*, int)>(&hipo::event::init), "init");
    event.def("getStructure", static_cast<void (hipo::event::*)(hipo::structure&, int, int)>(&hipo::event::getStructure), "getStructure");
    event.def("getStructure", static_cast<void (hipo::event::*)(hipo::bank&)>(&hipo::event::getStructure), "getStructure");
    // event.def_static("getStructure", static_cast<void (hipo::event::*)(const char*, hipo::structure&, int, int)>(&hipo::event::getStructure), "getStructure"); //TODO: //NOTE: Not sure why this doesn't work right now...
    event.def("getTag", &hipo::event::getTag);
    event.def("read", &hipo::event::read);
    event.def("addStructure", &hipo::event::addStructure);
    event.def("getStructurePosition", static_cast<std::pair<int,int> (hipo::event::*)(int, int)>(&hipo::event::getStructurePosition), "getStructurePosition");
    // event.def_static("getStructurePosition", static_cast<std::pair<int,int> (hipo::event::*)(const char*, int, int)>(&hipo::event::getStructurePosition), "getStructurePosition"); //TODO: //NOTE: Not sure why this doesn't work right now...  same as above is a static method maybe that is why...
    event.def("getEventBuffer", &hipo::event::getEventBuffer);
    event.def("getSize", &hipo::event::getSize);
    event.def("reset", &hipo::event::reset);
    event.def("getStructureNoCopy", &hipo::event::getStructureNoCopy);

    // event.def_property_readonly("databuffer", nullptr); //NOTE: Not really necessary.

    event.def("__repr__", //TODO: Test this function in python
             [](hipo::event &e) {
                std::string r("Event : size = "); r += std::to_string(e.getSize())+"\n";
                int position = 16;
                int eventSize = *(reinterpret_cast<uint32_t*>(&e.getEventBuffer()[4]));
                while(position+8<eventSize) {
                    uint16_t   gid = *(reinterpret_cast<uint16_t*>(&e.getEventBuffer()[position]));
                    uint8_t    iid = *(reinterpret_cast<uint8_t*>(&e.getEventBuffer()[position+2]));
                    uint8_t   type = *(reinterpret_cast<uint8_t*>(&e.getEventBuffer()[position+3]));
                    int     length = *(reinterpret_cast<int*>(&e.getEventBuffer()[position+4]));
                    r += "\tgroup = "+std::to_string(gid)+" , item = "+std::to_string(iid)+" , type = "+std::to_string(type)+" , length = "+std::to_string(length)+"\n";
                    position += (length + 8);
                }
                return r;
            } // [](hipo::event &e)
    );
    event.def("__eq__", //TODO: Test this function in python
        [](hipo::event *e1, hipo::event *e2) { return e1 == e2; }
    );
    event.def("__len__", //TODO: Test this function in python
        [](hipo::event &e) { return e.getSize(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO readerIndex
    py::class_<hipo::readerIndex> readerIndex(m, "ReaderIndex"); //NOTE: Can't use trampoline class because you get this error: "Cannot use an alias class with a non-polymorphic type"
    readerIndex.def(py::init<>([]() { return new hipo::readerIndex(); }));

    readerIndex.def("canAdvance", &hipo::readerIndex::canAdvance);
    readerIndex.def("advance", &hipo::readerIndex::advance);

    readerIndex.def("canAdvanceInRecord", &hipo::readerIndex::canAdvanceInRecord);
    readerIndex.def("loadRecord", &hipo::readerIndex::loadRecord);
    readerIndex.def("gotoEvent", &hipo::readerIndex::gotoEvent);
    readerIndex.def("gotoRecord", &hipo::readerIndex::gotoRecord);

    readerIndex.def("getEventNumber", &hipo::readerIndex::getEventNumber);
    readerIndex.def("getRecordNumber", &hipo::readerIndex::getRecordNumber);
    readerIndex.def("getRecordEventNumber", &hipo::readerIndex::getRecordEventNumber);
    readerIndex.def("getMaxEvents", &hipo::readerIndex::getMaxEvents);
    readerIndex.def("addSize", &hipo::readerIndex::addSize);
    readerIndex.def("addPosition", &hipo::readerIndex::addPosition);
    readerIndex.def("getPosition", &hipo::readerIndex::getPosition);

    readerIndex.def("getNRecords", &hipo::readerIndex::getNRecords);
    readerIndex.def("rewind", &hipo::readerIndex::rewind);
    readerIndex.def("clear", &hipo::readerIndex::clear);
    readerIndex.def("reset", &hipo::readerIndex::reset);
    
    // readerIndex.def_property_readonly("recordEvents", nullptr); //NOTE: Not really necessary.
    // readerIndex.def_property_readonly("recordPosition", nullptr);
    readerIndex.def_property_readonly("currentRecord", &hipo::readerIndex::getRecordNumber);
    readerIndex.def_property_readonly("currentEvent", &hipo::readerIndex::getEventNumber);
    readerIndex.def_property_readonly("currentRecordEvent", &hipo::readerIndex::getRecordEventNumber);

    readerIndex.def("__repr__",
        [](hipo::readerIndex &r){
            std::string x("Reader Index : ");
            x += "nrecords = "+std::to_string(r.getNRecords())+" , record number = "+std::to_string(r.getRecordNumber())+" , event number = "+std::to_string(r.getEventNumber())+"\n";
            return x;
        }
    );

    readerIndex.def("__eq__", //TODO: Test this function in python
        [](hipo::readerIndex *r1, hipo::readerIndex *r2) { return r1 == r2; }
    );
    readerIndex.def("__len__", //TODO: Test this function in python
        [](hipo::readerIndex &r) { return r.getNRecords(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO reader
    py::class_<hipo::reader> reader(m, "Reader");
    reader.def(py::init<>([]() { return new hipo::reader(); }));
    reader.def(py::init([](const hipo::reader &r) { return new hipo::reader(r); }));

    reader.def("about", &hipo::reader::about);
    reader.def("readDictionary", &hipo::reader::readDictionary);
    reader.def("getStructure", &hipo::reader::getStructure);
    reader.def("getStructureNoCopy", &hipo::reader::getStructureNoCopy);
    reader.def("open", &hipo::reader::open);
    reader.def("setTags", static_cast<void (hipo::reader::*)(int)>(&hipo::reader::setTags), "setTags");
    reader.def("setTags", static_cast<void (hipo::reader::*)(std::vector<long>)>(&hipo::reader::setTags), "setTags");
    reader.def("setVerbose", &hipo::reader::setVerbose);

    reader.def("hasNext", &hipo::reader::hasNext);
    reader.def("next", static_cast<bool (hipo::reader::*)()>(&hipo::reader::next), "next");
    reader.def("next", static_cast<bool (hipo::reader::*)(hipo::event&)>(&hipo::reader::next), "next");
    reader.def("gotoEvent", &hipo::reader::gotoEvent);
    reader.def("gotoRecord", &hipo::reader::gotoRecord);
    reader.def("read", &hipo::reader::read);
    reader.def("printWarning", &hipo::reader::printWarning);

    reader.def("getNRecords", &hipo::reader::getNRecords);
    reader.def("nextInRecord", &hipo::reader::nextInRecord);
    reader.def("loadRecord", &hipo::reader::loadRecord);
    reader.def("getEntries", &hipo::reader::getEntries);

    reader.def("__repr__",
        [](hipo::reader &r){
            std::string x("Reader : ");
            x += "nrecords = "+std::to_string(r.getNRecords())+" , entries = "+std::to_string(r.getEntries())+"\n";
            return x;
        }
    );
    reader.def("__eq__", //TODO: Test this function in python
        [](hipo::reader *r1, hipo::reader *r2) { return r1 == r2; }
    );
    reader.def("__len__", //TODO: Test this function in python
        [](hipo::reader &r) { return r.getNRecords(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO data
    py::class_<hipo::data> data(m, "Data");
    data.def(py::init<>());

    data.def("setDataPtr", &hipo::data::setDataPtr);
    data.def("setDataSize", &hipo::data::setDataSize);
    data.def("setDataOffset", &hipo::data::setDataOffset);
    data.def("setDataEndianness", &hipo::data::setDataEndianness);

    data.def("getEvioPtr", &hipo::data::getEvioPtr);
    data.def("getEvioSize", &hipo::data::getEvioSize);
    data.def("getDataPtr", &hipo::data::getDataPtr);
    data.def("getDataSize", &hipo::data::getDataSize);
    data.def("getDataOffset", &hipo::data::getDataOffset);
    data.def("getDataEndianness", &hipo::data::getDataEndianness);

    data.def_property_readonly("data_ptr", &hipo::data::getDataPtr);
    data.def_property_readonly("data_size", &hipo::data::getDataSize);
    data.def_property_readonly("data_endianness", &hipo::data::getDataEndianness);
    data.def_property_readonly("data_offset", &hipo::data::getDataOffset);

    data.def("__repr__",
        [](hipo::data &d){
            std::string r("Data : ");
            r += "size = "+std::to_string(d.getDataSize())+"\n";
            return r;
        }
    );
    data.def("__eq__", //TODO: Test this function in python
        [](hipo::data *d1, hipo::data *d2) { return d1 == d2; }
    );
    data.def("__len__", //TODO: Test this function in python
        [](hipo::data &d) { return d.getDataSize(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO record
    py::class_<hipo::record> record(m, "Record");
    record.def(py::init<>());

    record.def("readRecord", static_cast<void (hipo::record::*)(std::ifstream&, long, int)>(&hipo::record::readRecord), "readRecord");
    record.def("readRecord", static_cast<bool (hipo::record::*)(std::ifstream&, long, int, long)>(&hipo::record::readRecord), "readRecord");
    record.def("readRecord__", &hipo::record::readRecord__);
    record.def("getEventCount", &hipo::record::getEventCount);
    record.def("getRecordSizeCompressed", &hipo::record::getRecordSizeCompressed);

    record.def("readEvent", &hipo::record::readEvent);
    record.def("readHipoEvent", &hipo::record::readHipoEvent);
    record.def("getData", &hipo::record::getData);

    record.def("getReadBenchmark", &hipo::record::getReadBenchmark);
    record.def("getUnzipBenchmark", &hipo::record::getUnzipBenchmark);
    record.def("getIndexBenchmark", &hipo::record::getIndexBenchmark);

    record.def_property_readonly("readBenchmark", &hipo::record::getReadBenchmark);
    record.def_property_readonly("unzipBenchmark", &hipo::record::getUnzipBenchmark);
    record.def_property_readonly("indexBenchmark", &hipo::record::getIndexBenchmark);

    record.def("__repr__",
        [](hipo::record &r){
            std::string x("Record : ");
            x += "event count = "+std::to_string(r.getEventCount())+"\n";
            return x;
        }
    );
    record.def("__eq__", //TODO: Test this function in python
        [](hipo::record *r1, hipo::record *r2) { return r1 == r2; }
    );
    record.def("__len__", //TODO: Test this function in python
        [](hipo::record &r) { return r.getEventCount(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO recordbuilder
    py::class_<hipo::recordbuilder, PyRecordBuilder<>> recordbuilder(m, "RecordBuilder");
    recordbuilder.def(py::init<>([]() { return new hipo::recordbuilder(); }));
    recordbuilder.def(py::init<>([](int maxEvents, int maxLength) { return new hipo::recordbuilder(maxEvents,maxLength); }));

    recordbuilder.def("addEvent", static_cast<bool (hipo::recordbuilder::*)(hipo::event&)>(&hipo::recordbuilder::addEvent), "addEvent");
    recordbuilder.def("addEvent", static_cast<bool (hipo::recordbuilder::*)(std::vector<char>&, int, int)>(&hipo::recordbuilder::addEvent), "addEvent");

    recordbuilder.def("getUserWordOne", &hipo::recordbuilder::getUserWordOne);
    recordbuilder.def("getUserWordTwo", &hipo::recordbuilder::getUserWordTwo);
    recordbuilder.def("setUserWordOne", &hipo::recordbuilder::setUserWordOne);
    recordbuilder.def("setUserWordTwo", &hipo::recordbuilder::setUserWordTwo);

    recordbuilder.def("getRecordSize", &hipo::recordbuilder::getRecordSize);
    recordbuilder.def("getEntries", &hipo::recordbuilder::getEntries);
    recordbuilder.def("getRecordBuffer", &hipo::recordbuilder::getRecordBuffer);
    recordbuilder.def("reset", &hipo::recordbuilder::reset);
    recordbuilder.def("build", &hipo::recordbuilder::build);

    recordbuilder.def_property_readonly("bufferUserWordOne", &hipo::recordbuilder::getUserWordOne);
    recordbuilder.def_property_readonly("bufferUserWordTwo", &hipo::recordbuilder::getUserWordTwo);

    recordbuilder.def("__repr__",
        [](hipo::recordbuilder &r){
            std::string x("Recordbuilder : ");
            x += "entries = "+std::to_string(r.getEntries())+" , userWordOne = "+std::to_string(r.getUserWordOne())+" , userWordTwo = "+std::to_string(r.getUserWordTwo())+"\n";
            return x;
        }
    );
    recordbuilder.def("__eq__", //TODO: Test this function in python
        [](hipo::recordbuilder *r1, hipo::recordbuilder *r2) { return r1 == r2; }
    );
    recordbuilder.def("__len__", //TODO: Test this function in python
        [](hipo::recordbuilder &r) { return r.getEntries(); }
    );

    //----------------------------------------------------------------------//
    // Bind HIPO writer
    py::class_<hipo::writer, PyWriter<>> writer(m, "Writer");
    writer.def(py::init<>([]() { return new hipo::writer(); }));

    writer.def("addEvent", static_cast<void (hipo::writer::*)(hipo::event&)>(&hipo::writer::addEvent), "addEvent");
    writer.def("addEvent", static_cast<void (hipo::writer::*)(std::vector<char>&, int)>(&hipo::writer::addEvent), "addEvent");
    writer.def("writeRecord", &hipo::writer::writeRecord);
    writer.def("open", &hipo::writer::open);
    writer.def("close", &hipo::writer::close);
    writer.def("showSummary", &hipo::writer::showSummary);
    writer.def("addDictionary", &hipo::writer::addDictionary);
    writer.def("getDictionary", &hipo::writer::getDictionary);
    writer.def("setUserIntegerOne", &hipo::writer::setUserIntegerOne);
    writer.def("setUserIntegerTwo", &hipo::writer::setUserIntegerTwo);
    writer.def("flush", &hipo::writer::flush);

    writer.def_property_readonly("writerDictionary", &hipo::writer::getDictionary);

    writer.def("__repr__",
        [](hipo::writer &w){
            std::string r("Writer : ");
            return r+"\n";
        }
    );
    writer.def("__eq__", //TODO: Test this function in python
        [](hipo::writer *w1, hipo::writer *w2) { return w1 == w2; }
    );

    //----------------------------------------------------------------------//
    // Documentation
    
    // m.doc() = R"pbdoc(
    //     HipopyBind plugin
    //     -----------------

    //     .. currentmodule:: hipopybind

    //     .. autosummary::
    //        :toctree: _generate

    //        add
    //        subtract
    // )pbdoc";

    // m.def("add", &add, R"pbdoc(
    //     Add two numbers

    //     Some other explanation about the add function.
    // )pbdoc");

    // m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
    //     Subtract two numbers

    //     Some other explanation about the subtract function.
    // )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
} //PYBIND11_MODULE
