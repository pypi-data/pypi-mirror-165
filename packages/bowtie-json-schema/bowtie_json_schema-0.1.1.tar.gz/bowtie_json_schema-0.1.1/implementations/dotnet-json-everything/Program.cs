using System;
using System.IO;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;


string line;
while ((line = Console.In.ReadLine()) != null && line != "") {
    JsonDocument document = JsonDocument.Parse(line);
    Console.Out.WriteLine(document);
}


Console.Out.WriteLine(RuntimeInformation.FrameworkDescription);

const long Mebi = 1024 * 1024;
const long Gibi = Mebi * 1024;
GCMemoryInfo gcInfo = GC.GetGCMemoryInfo();
long totalMemoryBytes = gcInfo.TotalAvailableMemoryBytes;

// Environment information
Console.Out.WriteLine($"{nameof(RuntimeInformation.OSArchitecture)}: {RuntimeInformation.OSArchitecture}");
Console.Out.WriteLine($"{nameof(Environment.ProcessorCount)}: {Environment.ProcessorCount}");
Console.Out.WriteLine($"{nameof(GCMemoryInfo.TotalAvailableMemoryBytes)}: {totalMemoryBytes}");

// cgroup information
if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux) && 
    Directory.Exists("/sys/fs/cgroup/cpu") &&
    Directory.Exists("/sys/fs/cgroup/memory") &&
    File.Exists("sys/fs/cgroup/cpu/cpu.cfs_quota_us"))
{
    // get cpu cgroup information
    string cpuquota = File.ReadAllLines("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")[0];
    if (int.TryParse(cpuquota, out int quota) &&
        quota > 0)
    {
        Console.Out.WriteLine($"cfs_quota_us: {quota}");
    }

    // get memory cgroup information
    string usageBytes = File.ReadAllLines("/sys/fs/cgroup/memory/memory.usage_in_bytes")[0];
    string limitBytes = File.ReadAllLines("/sys/fs/cgroup/memory/memory.limit_in_bytes")[0];
    if (long.TryParse(usageBytes, out long usage) &&
        long.TryParse(limitBytes, out long limit) &&
        // above this size is unlikely to be an intentionally constrained cgroup
        limit < 10 * Gibi)
    {
        Console.Out.WriteLine($"usage_in_bytes: {usageBytes} {usage}");
        Console.Out.WriteLine($"limit_in_bytes: {limitBytes} {limit}");
        Console.Out.WriteLine($"GC Hard limit %:  {decimal.Divide(totalMemoryBytes,limit) * 100}");
    }
}
