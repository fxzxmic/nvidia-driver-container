%if 0%{?__isa_bits} == 64
%global elf_bits (64bit)
%endif

Name:                   nvidia-driver
Version:                550.144.03
Release:                1
Summary:                NVIDIA binary driver for Linux container
License:                NVIDIA
URL:                    http://www.nvidia.com/
Source0:                https://download.nvidia.com/XFree86/Linux-%{_arch}/%{version}/NVIDIA-Linux-%{_arch}-%{version}-no-compat32.run
Source1:                https://download.nvidia.com/XFree86/Linux-%{_arch}/%{version}/NVIDIA-Linux-%{_arch}-%{version}-no-compat32.run.sha256sum

BuildRequires:          jq

Requires:               libnvidia-egl-wayland.so.1()%{?elf_bits}
Requires:               libnvidia-egl-gbm.so.1()%{?elf_bits}

ExclusiveArch:          x86_64

%description
The NVIDIA Linux graphics driver.

%prep
cd %{_sourcedir}
# Verify sha256sum
sha256sum -c %{SOURCE1}

rm -r %{_builddir}
sh %{SOURCE0} --extract-only --target %{_builddir}

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_libdir}/nvidia
mkdir -p %{buildroot}%{_libdir}/gbm
mkdir -p %{buildroot}%{_datadir}/nvidia
mkdir -p %{buildroot}%{_datadir}/nvidia/vulkan
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d

install -Dm0644 /dev/null -t %{buildroot}%{_datadir}/vulkan/icd.d/nvidia_icd.json
install -Dm0644 /dev/null -t %{buildroot}%{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json

mv libnvidia-gpucomp.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-api.so.* %{buildroot}%{_libdir}/nvidia
mv libnvidia-glcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-tls.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia_icd.json %{buildroot}%{_datadir}/nvidia/vulkan
mv nvidia_layers.json %{buildroot}%{_datadir}/nvidia/vulkan
mv nvidia-application-profiles-%{version}-* %{buildroot}%{_datadir}/nvidia
mv libnvidia-glsi.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glvkspirv.so.%{version} %{buildroot}%{_libdir}/nvidia
mv 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mv libnvidia-eglcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libEGL_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libGLESv2_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libGLESv1_CM_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-allocator.so.%{version} %{buildroot}%{_libdir}/nvidia

jq .ICD.library_path=\"libEGL_nvidia.so.0\" %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_icd.json > %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_icd.json
jq .layers[0].library_path=\"libEGL_nvidia.so.0\" %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_layers.json > %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_layers.json
# No X11 support
rm %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_icd.json
rm %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_layers.json

# Create symbolic links
cd %{buildroot}%{_libdir}
ln -sr nvidia/libnvidia-gpucomp.so.%{version} libnvidia-gpucomp.so.%{version}
ln -sr nvidia/libnvidia-api.so.* libnvidia-api.so.1
ln -sr nvidia/libnvidia-glcore.so.%{version} libnvidia-glcore.so.%{version}
ln -sr nvidia/libnvidia-tls.so.%{version} libnvidia-tls.so.%{version}
ln -sr nvidia/libnvidia-glsi.so.%{version} libnvidia-glsi.so.%{version}
ln -sr nvidia/libnvidia-glvkspirv.so.%{version} libnvidia-glvkspirv.so.%{version}
ln -sr nvidia/libnvidia-eglcore.so.%{version} libnvidia-eglcore.so.%{version}
ln -sr nvidia/libEGL_nvidia.so.%{version} libEGL_nvidia.so.0
ln -sr nvidia/libGLESv2_nvidia.so.%{version} libGLESv2_nvidia.so.2
ln -sr nvidia/libGLESv1_CM_nvidia.so.%{version} libGLESv1_CM_nvidia.so.1
ln -sr nvidia/libnvidia-allocator.so.%{version} libnvidia-allocator.so.1
ln -sr libnvidia-allocator.so.1 gbm/nvidia-drm_gbm.so
ln -sr libnvidia-allocator.so.1 libnvidia-allocator.so

%post
update-alternatives --install %{_datadir}/vulkan/icd.d/nvidia_icd.json nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/egl-nvidia_icd.json 25 --slave %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json nvidia-vulkan-layers %{_datadir}/nvidia/vulkan/egl-nvidia_layers.json

%preun
if [ $1 -eq 0 ]; then
    update-alternatives --remove nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/egl-nvidia_icd.json || :
fi

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.txt
%doc NVIDIA_Changelog
%dir %{_libdir}/nvidia
%{_libdir}/nvidia/libnvidia-gpucomp.so.%{version}
%{_libdir}/libnvidia-gpucomp.so.%{version}
%{_libdir}/nvidia/libnvidia-api.so.*
%{_libdir}/libnvidia-api.so.1
%{_libdir}/nvidia/libnvidia-glcore.so.%{version}
%{_libdir}/libnvidia-glcore.so.%{version}
%{_libdir}/nvidia/libnvidia-tls.so.%{version}
%{_libdir}/libnvidia-tls.so.%{version}
%{_libdir}/nvidia/libnvidia-glsi.so.%{version}
%{_libdir}/libnvidia-glsi.so.%{version}
%{_libdir}/nvidia/libnvidia-glvkspirv.so.%{version}
%{_libdir}/libnvidia-glvkspirv.so.%{version}
%{_libdir}/nvidia/libGLESv2_nvidia.so.%{version}
%{_libdir}/libGLESv2_nvidia.so.2
%{_libdir}/nvidia/libGLESv1_CM_nvidia.so.%{version}
%{_libdir}/libGLESv1_CM_nvidia.so.1
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-*
# nvidia-egl
%{_libdir}/nvidia/libnvidia-eglcore.so.%{version}
%{_libdir}/libnvidia-eglcore.so.%{version}
%{_libdir}/nvidia/libEGL_nvidia.so.%{version}
%{_libdir}/libEGL_nvidia.so.0
%ghost %{_datadir}/vulkan/icd.d/nvidia_icd.json
%ghost %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json
%{_datadir}/glvnd/egl_vendor.d/*
%{_datadir}/nvidia/vulkan/egl-nvidia_icd.json
%{_datadir}/nvidia/vulkan/egl-nvidia_layers.json
# nvidia-gbm
%dir %{_libdir}/gbm
%{_libdir}/gbm/*
%{_libdir}/nvidia/libnvidia-allocator.so.%{version}
%{_libdir}/libnvidia-allocator.so.1
%{_libdir}/libnvidia-allocator.so

%changelog
