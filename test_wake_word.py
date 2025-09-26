"""
Test wake-up word detection to debug the issue
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_porcupine_initialization():
    """Test if Porcupine can be initialized"""
    print("🧪 Testing Porcupine Initialization...")
    
    try:
        import pvporcupine
        
        # Check if access key is available
        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        print(f"✅ PORCUPINE_ACCESS_KEY: {'SET' if access_key else 'NOT SET'}")
        
        if not access_key:
            print("❌ No access key found")
            return False
        
        # Try to initialize Porcupine
        print("🔧 Initializing Porcupine...")
        porcupine = pvporcupine.create(
            keywords=["hey siri"],
            access_key=access_key,
            sensitivities=[0.5]
        )
        
        print("✅ Porcupine initialized successfully!")
        print(f"📊 Frame length: {porcupine.frame_length}")
        print(f"📊 Sample rate: {porcupine.sample_rate}")
        
        # Clean up
        porcupine.delete()
        print("✅ Porcupine test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Porcupine initialization failed: {e}")
        return False

def test_audio_devices():
    """Test if audio devices are available"""
    print("\n🧪 Testing Audio Devices...")
    
    try:
        import pyaudio
        
        pa = pyaudio.PyAudio()
        print(f"✅ PyAudio version: {pyaudio.__version__}")
        
        # List audio devices
        print("📱 Available audio devices:")
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  - Device {i}: {info['name']} (inputs: {info['maxInputChannels']})")
        
        pa.terminate()
        return True
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def test_microphone_access():
    """Test if we can access the microphone"""
    print("\n🧪 Testing Microphone Access...")
    
    try:
        import pyaudio
        import numpy as np
        
        pa = pyaudio.PyAudio()
        
        # Try to open a stream
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("✅ Microphone access successful!")
        
        # Try to read some audio
        print("🎤 Testing audio capture...")
        data = stream.read(1024)
        audio_data = np.frombuffer(data, dtype=np.int16)
        print(f"📊 Audio data length: {len(audio_data)}")
        print(f"📊 Audio level: {np.mean(np.abs(audio_data))}")
        
        stream.stop_stream()
        stream.close()
        pa.terminate()
        
        return True
        
    except Exception as e:
        print(f"❌ Microphone access failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Wake-up Word Detection Debug Test")
    print("=" * 50)
    
    # Test 1: Porcupine initialization
    porcupine_ok = test_porcupine_initialization()
    
    # Test 2: Audio devices
    audio_ok = test_audio_devices()
    
    # Test 3: Microphone access
    mic_ok = test_microphone_access()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"  Porcupine: {'✅' if porcupine_ok else '❌'}")
    print(f"  Audio Devices: {'✅' if audio_ok else '❌'}")
    print(f"  Microphone: {'✅' if mic_ok else '❌'}")
    
    if porcupine_ok and audio_ok and mic_ok:
        print("\n🎉 All tests passed! Wake-up word detection should work.")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()
